#*********************************************************************************#
# This file contains all the helper functions the command line interface utilizes #
#*********************************************************************************#
import csv
from fastapi import Depends
from datetime import datetime, date

from sqlalchemy.sql.functions import mode
import applicant.schemas as schemas, applicant.models as models, applicant.database as database
from applicant.database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

# Create the tables if they don't exist
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Yield returns a generator rather than returning the sqlalchemy db session that we require
# To fix the code we need to call the internal __next__ function in some form on the generator object returned from get_db
# This keeps sqlalchemy happy
db_gen = get_db()
db = next(db_gen)
# Function that reads passed assignment CSV files
def read_csv_assignment(csvfile) -> List[List]:
    output = []
    with open(csvfile, 'r') as file:
        reader = csv.reader(file)
        line_count = 0
        for row in reader:
            if line_count != 0:
                name = row[0]
                email = row[1]
                #Figuring out assigned teams
                if (row[2] != ""):
                    team_assigned = "Quantitative Research"
                    assignment_no = row[2]
                elif (row[3] != ""):
                    team_assigned = "Strategy Implementation"
                    assignment_no = row[3]
                elif (row[4] != ""):
                    team_assigned = "Software Development"
                    assignment_no = row[4]
                elif (row[5] != ""):
                    team_assigned = "Business"
                    assignment_no = row[5]

                date_given = string_to_date(row[6])
                date_due = string_to_date(row[7])
                inner = [name, email, team_assigned, assignment_no, date_given, date_due]
                output.append(inner)
            else:
                line_count += 1 #Skip the column headers
    return output

# Function that reads passed submission CSV files
def read_csv_submission(csvfile) -> List[List]:
    output = []
    with open(csvfile, 'r') as file:
        reader = csv.reader(file)
        line_count = 0
        for row in reader:
            if line_count != 0:
                name = row[3]
                netid = row[4]
                email = row[2]
                year = row[5]
                major = row[6]
                smajor = row[7]
                minor = row[8]
                sminor = row[9]
                teams = row[12]
                inner = [name, netid, email, year, major, smajor, teams, minor, sminor]
                output.append(inner)
            else:
                line_count += 1 #Skip the column headers
    return output

# Function that enters passed data into the DB
def write_to_db(nestedAssignments: List[List], nestedSubmissions: List[List]) -> None:
    # Overwriting the tables by dropping previous ones
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)
    task_id_count = 1 # To assign assignments
    for assignment in nestedAssignments:
        for submission in nestedSubmissions:
            # Making sure assignments are given to those who pass initial screening
            if(assignment[0] == submission[0] and assignment[1] == submission[2]):
                new_assignment = models.AdditionalInfo(
                    assignment_no = assignment[3],
                    team_assigned = assignment[2],
                    date_due = assignment[5],
                    date_given = assignment[4]
                )
                db.add(new_assignment)
                db.commit()
                db.refresh(new_assignment)

                new_applicant = models.Applicant(
                    name = submission[0],
                    netid = submission[1],
                    email = submission[2],
                    year = submission[3],
                    major = submission[4],
                    smajor = submission[5],
                    teams = submission[6],
                    minor = submission[7],
                    sminor = submission[8],
                    task_id = task_id_count
                )
                db.add(new_applicant)
                db.commit()
                db.refresh(new_applicant)
                task_id_count += 1

# Convert strings to datetime.date objects
def string_to_date(date_string: str) -> datetime.date:
    d_format = "%Y-%m-%d"
    date_obj = datetime.strptime(date_string, d_format).date()
    return date_obj

# Give general overview of applicants
def overview_applicants():
    applicants = db.query(models.Applicant).order_by(models.Applicant.netid).count()
    print("Total Number of Applicants Given an Assignment:", applicants)
    did_not_submit_count = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.submitted == False).count()
    print("Total Number of Applicants That Haven't Done with Their Assignment:", did_not_submit_count)
    if did_not_submit_count > 0:
        print("Applicants Who Haven't Submitted Assignments:-")
        print("| NetID | Name | Assignment Number | Date Given | Date Due |")
        did_not_submit = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.submitted == False).all()
        for assignment in did_not_submit:
            person = db.query(models.Applicant).filter(models.Applicant.task_id == assignment.id).all()
            print(
                "|",person[0].netid, 
                person[0].name, 
                assignment.assignment_no, 
                assignment.date_given, 
                assignment.date_due,"|"
                )
    did_submit_count = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.submitted == True).count()
    print("Total Number of Applicants That Have Done Their Assignments:", did_submit_count)
    if did_submit_count > 0:
        print("Applicants Who Have Submitted Assignments:-")
        print("| NetID | Name | Assignment Number | Date Given | Date Due | Comments |")
        did_not_submit = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.submitted == True).all()
        for assignment in did_not_submit:
            person = db.query(models.Applicant).filter(models.Applicant.task_id == assignment.id).all()
            print(
                "|",person[0].netid, 
                person[0].name, 
                assignment.assignment_no, 
                assignment.date_given, 
                assignment.date_due,
                assignment.assignment_comments,"|"
                )
    
    overdue_count = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.date_due < date.today()).count()
    print("Applicants overdue on Assignments:", overdue_count)
    if overdue_count > 0:
        print("Applicants Who Are Overdue:-")
        print("| NetID | Name | Assignment Number | Date Given | Date Due | Comments |")
        overdue = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.date_due < date.today()).all()
        for assignment in overdue:
            person = db.query(models.Applicant).filter(models.Applicant.task_id == assignment.id).all()
            print(
                "|",person[0].netid, 
                person[0].name, 
                assignment.assignment_no, 
                assignment.date_given, 
                assignment.date_due,
                assignment.assignment_comments,"|"
                )

# Write Overview to txt file
def write_overview_to_applicants():
    with open("output.txt","w+") as file:
        applicants = db.query(models.Applicant).order_by(models.Applicant.netid).count()
        line = "Total Number of Applicants Given an Assignment:", str(applicants), "\n"
        file.writelines(line)
        did_not_submit_count = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.submitted == False).count()
        line = "Total Number of Applicants That Haven't Done with Their Assignment:",str(did_not_submit_count),"\n"
        file.writelines(line)

        if did_not_submit_count > 0:
            file.writelines("Applicants Who Haven't Submitted Assignments:-\n")
            file.writelines("| NetID | Name | Assignment Number | Date Given | Date Due |\n")
            did_not_submit = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.submitted == False).all()
            for assignment in did_not_submit:
                person = db.query(models.Applicant).filter(models.Applicant.task_id == assignment.id).all()
                line = "| " + person[0].netid + person[0].name + str(assignment.assignment_no) + str(assignment.date_given) + str(assignment.date_due)," |\n"
                file.writelines(line)
        
        did_submit_count = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.submitted == True).count()
        line = "Total Number of Applicants That Have Done Their Assignments:" + str(did_submit_count) + "\n"
        file.writelines(line)
        if did_submit_count > 0:
            file.writelines("Applicants Who Have Submitted Assignments:-\n")
            file.writelines("| NetID | Name | Assignment Number | Date Given | Date Due | Comments |\n")
            did_not_submit = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.submitted == True).all()
            for assignment in did_not_submit:
                person = db.query(models.Applicant).filter(models.Applicant.task_id == assignment.id).all()
                line = "| " + person[0].netid + person[0].name + str(assignment.assignment_no) + str(assignment.date_given) + str(assignment.date_due) + assignment.assignment_comments," |\n"
                file.writelines(line)

        overdue_count = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.date_due < date.today()).count()
        line = "Applicants overdue on Assignments: "+ str(overdue_count) +"\n"
        file.writelines(line)
        if overdue_count > 0:
            file.writelines("Applicants Who Are Overdue:-\n")
            file.writelines("| NetID | Name | Assignment Number | Date Given | Date Due | Comments |\n")
            overdue = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.date_due < date.today()).all()
            for assignment in overdue:
                person = db.query(models.Applicant).filter(models.Applicant.task_id == assignment.id).all()
                line = "| " + person[0].netid + person[0].name + str(assignment.assignment_no) + str(assignment.date_given) + str(assignment.date_due) + assignment.assignment_comments," |\n"
                file.writelines(line)

# Get applicant by netid
def get_by_netid(netid: str):
    applicant = db.query(models.Applicant).filter(models.Applicant.netid == netid).first()
    assignment = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.id == applicant.task_id).first()
    if not applicant:
        print("Applicant with netid ", netid, " not found")
    print("| NetID | Name | Email | Major | Assignment Number | Date Given | Date Due | Comments |")
    print("|", applicant.netid,
           applicant.name,
           applicant.email,
           applicant.major,
           assignment.assignment_no,
           assignment.date_given,
           assignment.date_due,
           assignment.assignment_comments,"|"
           )