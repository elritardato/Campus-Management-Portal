from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from database import Base
import enum

class UserTypeEnum(enum.Enum):
    Student = "Student"
    Faculty = "Faculty"

class Students(Base):
    __tablename__ = "STUDENTS"
    
    Student_ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    Department = Column(String(100))
    Year = Column(Integer)
    Contact = Column(String(15))
    Email = Column(String(100))

class Faculty(Base):
    __tablename__ = "FACULTY"
    
    Faculty_ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    Department = Column(String(100))
    Designation = Column(String(100))
    Contact = Column(String(15))
    Email = Column(String(100))

class Equipment(Base):
    __tablename__ = "EQUIPMENT"
    
    Equipment_ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    Category = Column(String(50))
    Purchase_Date = Column(Date)
    Condition_Status = Column(String(50))

class Location(Base):
    __tablename__ = "LOCATION"
    
    Location_ID = Column(Integer, primary_key=True, index=True)
    Location_Name = Column(String(100))
    Building = Column(String(100))
    Room_No = Column(String(20))

class EquipmentUsage(Base):
    __tablename__ = "EQUIPMENT_USAGE"
    
    Usage_ID = Column(Integer, primary_key=True, index=True)
    Equipment_ID = Column(Integer, ForeignKey("EQUIPMENT.Equipment_ID"))
    User_ID = Column(Integer)
    User_Type = Column(Enum(UserTypeEnum))
    Location_ID = Column(Integer, ForeignKey("LOCATION.Location_ID"))
    Date_CheckedOut = Column(Date)
    Date_Returned = Column(Date, nullable=True)
