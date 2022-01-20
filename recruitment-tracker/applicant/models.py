from sqlalchemy import Column, String, Boolean, Integer, Date, ForeignKey
from sqlalchemy.sql.schema import ForeignKey
from .database import Base
import datetime
from sqlalchemy.orm import relationship

class Applicant(Base):
    __tablename__ = "applicants"
    netid = Column(String, primary_key=True, index=True)
    selected = Column(Boolean, default=False)
    comments = Column(String, default="", nullable=True)
    name = Column(String)
    email = Column(String)
    year = Column(String)
    major = Column(String)
    smajor = Column(String, default="", nullable=True)
    teams = Column(String)
    minor = Column(String, default="", nullable=True)
    sminor = Column(String, default="", nullable=True)
    task_id = Column(Integer, ForeignKey('assignments.id'))
    #Relationship b/w tables
    task = relationship("AdditionalInfo", back_populates="person")

class AdditionalInfo(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    assignment_no = Column(String)
    team_assigned = Column(String)
    date_given = Column(Date)
    date_due = Column(Date)
    submitted = Column(Boolean, default=False)
    assignment_comments = Column(String, default="NA", nullable=True)
    #Relationship b/w tables
    person = relationship("Applicant", back_populates="task")