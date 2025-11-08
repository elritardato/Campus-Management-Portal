from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from pydantic import BaseModel

import models
from database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Equipment Location Tracker")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas
class StudentCreate(BaseModel):
    Student_ID: int
    Name: str
    Department: Optional[str] = None
    Year: Optional[int] = None
    Contact: Optional[str] = None
    Email: Optional[str] = None

class FacultyCreate(BaseModel):
    Faculty_ID: int
    Name: str
    Department: Optional[str] = None
    Designation: Optional[str] = None
    Contact: Optional[str] = None
    Email: Optional[str] = None

class EquipmentCreate(BaseModel):
    Equipment_ID: int
    Name: str
    Category: Optional[str] = None
    Purchase_Date: Optional[date] = None
    Condition_Status: Optional[str] = None

class LocationCreate(BaseModel):
    Location_ID: int
    Location_Name: Optional[str] = None
    Building: Optional[str] = None
    Room_No: Optional[str] = None

class CheckOutRequest(BaseModel):
    Equipment_ID: int
    User_ID: int
    User_Type: str
    Location_ID: int
    Date_CheckedOut: date

class CheckInRequest(BaseModel):
    Usage_ID: int
    Date_Returned: date

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Equipment Location Tracker API"}

# Students endpoints
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Students).all()
    return students

@app.post("/students")
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Students(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Students).filter(models.Students.Student_ID == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted"}

# Faculty endpoints
@app.get("/faculty")
def get_faculty(db: Session = Depends(get_db)):
    faculty = db.query(models.Faculty).all()
    return faculty

@app.post("/faculty")
def add_faculty(faculty: FacultyCreate, db: Session = Depends(get_db)):
    db_faculty = models.Faculty(**faculty.dict())
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty

@app.delete("/faculty/{faculty_id}")
def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    faculty = db.query(models.Faculty).filter(models.Faculty.Faculty_ID == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    db.delete(faculty)
    db.commit()
    return {"message": "Faculty deleted"}

# Equipment endpoints
@app.get("/equipment")
def get_equipment(db: Session = Depends(get_db)):
    equipment = db.query(models.Equipment).all()
    return equipment

@app.get("/equipment/{equipment_id}")
def get_equipment_by_id(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.query(models.Equipment).filter(models.Equipment.Equipment_ID == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@app.post("/equipment")
def add_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)):
    db_equipment = models.Equipment(**equipment.dict())
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

@app.delete("/equipment/{equipment_id}")
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.query(models.Equipment).filter(models.Equipment.Equipment_ID == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    db.delete(equipment)
    db.commit()
    return {"message": "Equipment deleted"}

# Location endpoints
@app.get("/locations")
def get_locations(db: Session = Depends(get_db)):
    locations = db.query(models.Location).all()
    return locations

@app.post("/locations")
def add_location(location: LocationCreate, db: Session = Depends(get_db)):
    db_location = models.Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@app.delete("/locations/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(models.Location).filter(models.Location.Location_ID == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(location)
    db.commit()
    return {"message": "Location deleted"}

# Equipment Usage endpoints
@app.get("/usage")
def get_all_usage(db: Session = Depends(get_db)):
    usage = db.query(models.EquipmentUsage).all()
    return usage

@app.get("/usage/checked_out")
def get_checked_out_equipment(db: Session = Depends(get_db)):
    usage = db.query(models.EquipmentUsage).filter(models.EquipmentUsage.Date_Returned == None).all()
    return usage

@app.get("/equipment/{equipment_id}/location")
def get_equipment_location(equipment_id: int, db: Session = Depends(get_db)):
    usage = db.query(models.EquipmentUsage).filter(
        models.EquipmentUsage.Equipment_ID == equipment_id,
        models.EquipmentUsage.Date_Returned == None
    ).first()
    
    if not usage:
        return {"message": "Equipment is not currently checked out"}
    
    location = db.query(models.Location).filter(models.Location.Location_ID == usage.Location_ID).first()
    equipment = db.query(models.Equipment).filter(models.Equipment.Equipment_ID == equipment_id).first()
    
    return {
        "Equipment_ID": equipment_id,
        "Equipment_Name": equipment.Name if equipment else None,
        "Location": location.Location_Name if location else None,
        "Building": location.Building if location else None,
        "Room_No": location.Room_No if location else None,
        "Checked_Out_Date": usage.Date_CheckedOut
    }

@app.post("/check_out")
def check_out_equipment(request: CheckOutRequest, db: Session = Depends(get_db)):
    existing = db.query(models.EquipmentUsage).filter(
        models.EquipmentUsage.Equipment_ID == request.Equipment_ID,
        models.EquipmentUsage.Date_Returned == None
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Equipment is already checked out")
    
    new_usage_id = db.query(models.EquipmentUsage).count() + 1
    
    new_usage = models.EquipmentUsage(
        Usage_ID=new_usage_id,
        Equipment_ID=request.Equipment_ID,
        User_ID=request.User_ID,
        User_Type=models.UserTypeEnum[request.User_Type],
        Location_ID=request.Location_ID,
        Date_CheckedOut=request.Date_CheckedOut,
        Date_Returned=None
    )
    
    db.add(new_usage)
    db.commit()
    db.refresh(new_usage)
    return new_usage

@app.post("/check_in")
def check_in_equipment(request: CheckInRequest, db: Session = Depends(get_db)):
    usage = db.query(models.EquipmentUsage).filter(models.EquipmentUsage.Usage_ID == request.Usage_ID).first()
    
    if not usage:
        raise HTTPException(status_code=404, detail="Usage record not found")
    
    if usage.Date_Returned is not None:
        raise HTTPException(status_code=400, detail="Equipment already checked in")
    
    usage.Date_Returned = request.Date_Returned
    db.commit()
    db.refresh(usage)
    return usage

# Dashboard stats
@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    return {
        "total_students": db.query(models.Students).count(),
        "total_faculty": db.query(models.Faculty).count(),
        "total_equipment": db.query(models.Equipment).count(),
        "total_locations": db.query(models.Location).count(),
        "checked_out": db.query(models.EquipmentUsage).filter(models.EquipmentUsage.Date_Returned == None).count(),
        "total_usage": db.query(models.EquipmentUsage).count()
    }
