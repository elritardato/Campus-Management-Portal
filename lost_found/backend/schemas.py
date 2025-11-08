from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemResponse(BaseModel):
    Item_ID: int
    Item_Name: str
    Description: Optional[str]
    Category: Optional[str]
    Image_Path: Optional[str]
    Date_Reported: datetime

class LostFoundResponse(BaseModel):
    Record_ID: int
    Item_ID: int
    Item_Name: str
    Description: Optional[str]
    Category: Optional[str]
    Image_Path: Optional[str]
    Reported_By: int
    Reporter_Name: str
    Status: str
    Location: Optional[str]
    Date_Reported: datetime
    Date_Updated: datetime

class StudentResponse(BaseModel):
    Student_ID: int
    Name: str
    Department: Optional[str]
    Year: Optional[int]
    Contact: Optional[str]
    Email: Optional[str]

class FacultyResponse(BaseModel):
    Faculty_ID: int
    Name: str
    Department: Optional[str]
    Designation: Optional[str]
    Contact: Optional[str]
    Email: Optional[str]