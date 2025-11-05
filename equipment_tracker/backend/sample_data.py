from datetime import date, timedelta
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

# Create tables
models.Base.metadata.create_all(bind=engine)

def add_sample_data():
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(models.EquipmentUsage).delete()
        db.query(models.Equipment).delete()
        db.query(models.Location).delete()
        db.query(models.Faculty).delete()
        db.query(models.Students).delete()
        db.commit()
        
        # Add Students
        students = [
            models.Students(Student_ID=1, Name="Rajesh Kumar", Department="Computer Science", Year=3, Contact="9876543210", Email="rajesh@university.edu"),
            models.Students(Student_ID=2, Name="Priya Sharma", Department="Electronics", Year=2, Contact="9876543211", Email="priya@university.edu"),
            models.Students(Student_ID=3, Name="Amit Patel", Department="Mechanical", Year=4, Contact="9876543212", Email="amit@university.edu"),
            models.Students(Student_ID=4, Name="Sneha Reddy", Department="Chemical", Year=1, Contact="9876543213", Email="sneha@university.edu"),
            models.Students(Student_ID=5, Name="Vikram Singh", Department="Civil", Year=3, Contact="9876543214", Email="vikram@university.edu")
        ]
        db.add_all(students)
        
        # Add Faculty
        faculty = [
            models.Faculty(Faculty_ID=101, Name="Dr. Anil Verma", Department="Computer Science", Designation="Professor", Contact="9123456789", Email="anil.verma@university.edu"),
            models.Faculty(Faculty_ID=102, Name="Dr. Meera Iyer", Department="Electronics", Designation="Associate Professor", Contact="9123456790", Email="meera.iyer@university.edu"),
            models.Faculty(Faculty_ID=103, Name="Dr. Ravi Desai", Department="Physics", Designation="Assistant Professor", Contact="9123456791", Email="ravi.desai@university.edu"),
            models.Faculty(Faculty_ID=104, Name="Dr. Sunita Joshi", Department="Chemistry", Designation="Professor", Contact="9123456792", Email="sunita.joshi@university.edu")
        ]
        db.add_all(faculty)
        
        # Add Equipment
        equipment = [
            models.Equipment(Equipment_ID=201, Name="Cricket Bat", Category="Sports", Purchase_Date=date(2023, 1, 15), Condition_Status="Good"),
            models.Equipment(Equipment_ID=202, Name="Football", Category="Sports", Purchase_Date=date(2023, 2, 20), Condition_Status="Good"),
            models.Equipment(Equipment_ID=203, Name="Guitar", Category="Music", Purchase_Date=date(2022, 8, 10), Condition_Status="Excellent"),
            models.Equipment(Equipment_ID=204, Name="Keyboard", Category="Music", Purchase_Date=date(2022, 9, 5), Condition_Status="Good"),
            models.Equipment(Equipment_ID=205, Name="Microscope", Category="Laboratory", Purchase_Date=date(2021, 5, 12), Condition_Status="Good"),
            models.Equipment(Equipment_ID=206, Name="Centrifuge", Category="Laboratory", Purchase_Date=date(2021, 6, 18), Condition_Status="Excellent"),
            models.Equipment(Equipment_ID=207, Name="Projector", Category="Event", Purchase_Date=date(2023, 3, 8), Condition_Status="Good"),
            models.Equipment(Equipment_ID=208, Name="Sound System", Category="Event", Purchase_Date=date(2023, 4, 22), Condition_Status="Excellent"),
            models.Equipment(Equipment_ID=209, Name="Tennis Racket", Category="Sports", Purchase_Date=date(2023, 5, 14), Condition_Status="Good"),
            models.Equipment(Equipment_ID=210, Name="Drums Set", Category="Music", Purchase_Date=date(2022, 11, 30), Condition_Status="Good")
        ]
        db.add_all(equipment)
        
        # Add Locations
        locations = [
            models.Location(Location_ID=301, Location_Name="Sports Complex", Building="Building A", Room_No="Ground Floor"),
            models.Location(Location_ID=302, Location_Name="Music Room", Building="Building B", Room_No="201"),
            models.Location(Location_ID=303, Location_Name="Chemistry Lab", Building="Building C", Room_No="301"),
            models.Location(Location_ID=304, Location_Name="Physics Lab", Building="Building C", Room_No="302"),
            models.Location(Location_ID=305, Location_Name="Auditorium", Building="Building D", Room_No="Main Hall"),
            models.Location(Location_ID=306, Location_Name="Biology Lab", Building="Building C", Room_No="303"),
            models.Location(Location_ID=307, Location_Name="Conference Room", Building="Building E", Room_No="401")
        ]
        db.add_all(locations)
        
        # Add Equipment Usage records
        today = date.today()
        usage_records = [
            models.EquipmentUsage(Usage_ID=1, Equipment_ID=201, User_ID=1, User_Type=models.UserTypeEnum.Student, Location_ID=301, Date_CheckedOut=today - timedelta(days=2), Date_Returned=None),
            models.EquipmentUsage(Usage_ID=2, Equipment_ID=203, User_ID=2, User_Type=models.UserTypeEnum.Student, Location_ID=302, Date_CheckedOut=today - timedelta(days=1), Date_Returned=None),
            models.EquipmentUsage(Usage_ID=3, Equipment_ID=207, User_ID=101, User_Type=models.UserTypeEnum.Faculty, Location_ID=305, Date_CheckedOut=today, Date_Returned=None),
            models.EquipmentUsage(Usage_ID=4, Equipment_ID=205, User_ID=103, User_Type=models.UserTypeEnum.Faculty, Location_ID=303, Date_CheckedOut=today - timedelta(days=10), Date_Returned=today - timedelta(days=8)),
            models.EquipmentUsage(Usage_ID=5, Equipment_ID=202, User_ID=3, User_Type=models.UserTypeEnum.Student, Location_ID=301, Date_CheckedOut=today - timedelta(days=7), Date_Returned=today - timedelta(days=5)),
            models.EquipmentUsage(Usage_ID=6, Equipment_ID=208, User_ID=102, User_Type=models.UserTypeEnum.Faculty, Location_ID=305, Date_CheckedOut=today - timedelta(days=15), Date_Returned=today - timedelta(days=14)),
            models.EquipmentUsage(Usage_ID=7, Equipment_ID=206, User_ID=104, User_Type=models.UserTypeEnum.Faculty, Location_ID=306, Date_CheckedOut=today - timedelta(days=20), Date_Returned=today - timedelta(days=18))
        ]
        db.add_all(usage_records)
        
        db.commit()
        print("✅ Sample data added successfully!")
        print(f"   - {len(students)} Students")
        print(f"   - {len(faculty)} Faculty")
        print(f"   - {len(equipment)} Equipment")
        print(f"   - {len(locations)} Locations")
        print(f"   - {len(usage_records)} Usage Records")
        print("\n📊 Database ready to use!")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_data()