from typing import final, List
from fastapi import FastAPI, Depends, Response, HTTPException, status
from . import schemas, models, database
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

# Create the tables if they don't exist
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create an applicant
@app.post('/applicant', response_model=schemas.ShowApplicant ,status_code=status.HTTP_201_CREATED, tags=['applicants'])
def create(request: schemas.Applicant, db: Session = Depends(get_db)):
    check_netid = db.query(models.Applicant).filter(models.Applicant.netid == request.netid).first()
    if (check_netid):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Applicant with netid "+request.netid+" already exists")
    check_task_id = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.id == request.task_id).first()
    if not check_task_id:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Task ID " + str(request.task_id) + " does not exist")
    new_applicant = models.Applicant(
        name=request.name,
        netid=request.netid,
        selected=request.selected,
        comments=request.comments,
        email=request.email,
        year=request.year,
        major=request.major,
        smajor=request.smajor,
        teams=request.teams,
        minor=request.minor,
        sminor=request.sminor,
        task_id=request.task_id # Assign relevant task id 
        )
    db.add(new_applicant)
    db.commit()
    db.refresh(new_applicant)
    return new_applicant

# Delete an applicant by their netid
@app.delete('/applicant/{netid}',tags=['applicants'])
def delete(netid: str, db: Session = Depends(get_db)):
    applicant = db.query(models.Applicant).filter(models.Applicant.netid == netid)
    if not applicant.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Applicant with netid '{netid}' not found")
    applicant.delete(synchronize_session=False)
    db.commit()
    return 'deleted'

# Update an applicant by their netid
@app.put('/applicant/{netid}', status_code=status.HTTP_202_ACCEPTED, tags=['applicants'])
def update(netid: str, request: schemas.Applicant, db: Session = Depends(get_db)):
    applicant = db.query(models.Applicant).filter(models.Applicant.netid == netid)
    if not applicant.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Applicant with netid '{netid}' does not exist")
    check_task_id = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.id == request.task_id).first()
    if not check_task_id:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Task ID " + str(request.task_id) + " does not exist")
    check_netid = db.query(models.Applicant).filter(models.Applicant.netid == request.netid).first()
    if (check_netid):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Applicant with netid "+request.netid+" already exists")
    applicant.update(request.dict())
    db.commit()
    return 'updated'

# Show all applicants
@app.get('/applicant',tags=['applicants'])
def all(db: Session = Depends(get_db)):
    applicants = db.query(models.Applicant).order_by(models.Applicant.netid).all()
    return applicants

# Search an applicant by their netid
@app.get('/applicant/{netid}', response_model=schemas.ShowApplicant, status_code=status.HTTP_202_ACCEPTED, tags=['applicants'])
def get_by_netid(netid: str, response: Response, db: Session = Depends(get_db)):
    applicant = db.query(models.Applicant).filter(models.Applicant.netid == netid).first()
    if not applicant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Applicant with netid '{netid}' not found")
    return applicant

# Create an assignment 
@app.post('/assignment', status_code=status.HTTP_202_ACCEPTED, tags=['assignments'])
def create_assignment(request: schemas.AdditionalInfo, db: Session = Depends(get_db)):
    assignment = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.id == request.id).first()
    if not assignment:
        new_assignment = models.AdditionalInfo(
        assignment_no = request.assignment_no,
        team_assigned = request.team_assigned,
        date_given = request.date_given,
        date_due = request.date_due,
        submitted = request.submitted,
        assignment_comments = request.assignment_comments,
        id = request.id
    )
        db.add(new_assignment)
        db.commit()
        db.refresh(new_assignment)
        return new_assignment
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"Assignment with this id already exists")

# Get everyone doing an assignment by task id
@app.get('/assignment/{id}', response_model= schemas.ShowAdditionalInfo, status_code=status.HTTP_202_ACCEPTED ,tags=['assignments'])
def get_assignment_by_id(id: int, db: Session = Depends(get_db)):
    assignment = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.id == id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Assignment with the id '{id}' is not available")
    return assignment

# Get an assignment by assignment no
@app.get('/assignments/{no}', response_model=List[schemas.ShowAdditionalInfo],status_code=status.HTTP_202_ACCEPTED, tags=['assignments'])
def get_by_assignment_number(no: str, db: Session = Depends(get_db)):
    assignments = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.assignment_no == no)
    #print(assignments.first().person)
    if len(assignments.all()) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Assignment with the assignment number '{no}' does not exist")
    result = [u for u in assignments.all()]
    return result
     
# Update a task by task id
@app.put('/assignment/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['assignments'])
def update(id: str, request: schemas.UpdateAdditionalInfo, db: Session = Depends(get_db)):
    applicant = db.query(models.AdditionalInfo).filter(models.AdditionalInfo.id == id)
    if not applicant.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Applicant with netid '{id}' does not exist")
    db.commit()
    return 'updated'