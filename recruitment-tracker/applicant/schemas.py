from pydantic import BaseModel
from typing import Optional, List

from sqlalchemy.sql.sqltypes import DateTime
import datetime

class Applicant(BaseModel):
    name: str
    netid: str
    selected: bool = False
    comments: Optional[str] = ""
    email: str
    year: str
    major: str
    smajor: Optional[str] = ""
    teams: str
    minor: Optional[str] = ""
    sminor: Optional[str] = ""
    task_id: int

    class Config():
        orm_mode = True

class AdditionalInfo(BaseModel):
    id: int
    assignment_no: str
    team_assigned: str
    date_given: datetime.date
    date_due: datetime.date
    submitted: bool = False
    assignment_comments: Optional[str] = "NA"  

    class Config():
        orm_mode = True

class UpdateAdditionalInfo(BaseModel):
    assignment_no: str
    team_assigned: str
    date_given: datetime.date
    date_due: datetime.date
    submitted: bool = False
    assignment_comments: Optional[str] = "NA"  

    class Config():
        orm_mode = True
# Response Models:

class ShowApplicant(BaseModel):
    name: str
    netid: str
    selected: bool = False
    comments: Optional[str] = ""
    email: str
    year: str
    major: str
    smajor: Optional[str] = ""
    teams: str
    minor: Optional[str] = ""
    sminor: Optional[str] = ""
    task_id: int
    task: AdditionalInfo

    class Config():
        orm_mode = True

class ShowAdditionalInfo(BaseModel):
    id: int
    assignment_no: str
    team_assigned: str
    date_given: datetime.date
    date_due: datetime.date
    submitted: bool = False
    assignment_comments: Optional[str] = "NA"  
    person: List[Applicant] = []

    class Config():
        orm_mode = True