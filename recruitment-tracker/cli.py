# Import all the relevant functions from helper.py
#from applicant.helpers import read_csv_assignment, read_csv_submission, write_to_db, overview_applicants, write_overview_to_applicants, get_by_netid
from applicant.helpers import *
import typer

app = typer.Typer()

# Populate database by passing 2 CSV files
@app.command()
def init(file_assignment: str, file_submission: str):
    try: 
        assignments = read_csv_assignment(file_assignment)
        submissions = read_csv_submission(file_submission)
        write_to_db(assignments, submissions)
        print("Succesfully Added Records To The Database")
    except Exception as e:
        print("Something Went Wrong Populating The Database. Error: ",e)

# Get an Applicant Overview
@app.command()
def overview(output_to_file: bool = False):
    try:
        overview_applicants()
        if output_to_file == True:
            write_overview_to_applicants()
    except Exception as e:
        print("Something Went Wrong Generating an Overview. Error: ",e)

# Search By Netid
@app.command()
def search(netid: str):
    try:
        get_by_netid(netid)
    except Exception as e:
        print("Something Went Wrong Getting the Applicant. Error: ",e)

if __name__ == "__main__":
    app()