-- Equipment Location Tracker Database Schema
-- This file is for reference; tables are created automatically by SQLAlchemy

CREATE TABLE STUDENTS (
    Student_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Department TEXT,
    Year INTEGER,
    Contact TEXT,
    Email TEXT
);

CREATE TABLE FACULTY (
    Faculty_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Department TEXT,
    Designation TEXT,
    Contact TEXT,
    Email TEXT
);

CREATE TABLE EQUIPMENT (
    Equipment_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Category TEXT,
    Purchase_Date TEXT,
    Condition_Status TEXT
);

CREATE TABLE LOCATION (
    Location_ID INTEGER PRIMARY KEY,
    Location_Name TEXT,
    Building TEXT,
    Room_No TEXT
);

CREATE TABLE EQUIPMENT_USAGE (
    Usage_ID INTEGER PRIMARY KEY,
    Equipment_ID INTEGER,
    User_ID INTEGER,
    User_Type TEXT CHECK(User_Type IN ('Student', 'Faculty')),
    Location_ID INTEGER,
    Date_CheckedOut TEXT,
    Date_Returned TEXT,
    FOREIGN KEY (Equipment_ID) REFERENCES EQUIPMENT(Equipment_ID),
    FOREIGN KEY (Location_ID) REFERENCES LOCATION(Location_ID)
);

-- Sample Data Insertions

-- Insert Sample Students
INSERT INTO STUDENTS (Name, Department, Year, Contact, Email) VALUES
('John Smith', 'Computer Science', 3, '555-0101', 'john.smith@university.edu'),
('Emily Davis', 'Electronics', 2, '555-0102', 'emily.davis@university.edu'),
('Michael Brown', 'Mechanical', 4, '555-0103', 'michael.brown@university.edu'),
('Sarah Wilson', 'Computer Science', 1, '555-0104', 'sarah.wilson@university.edu');

-- Insert Sample Faculty
INSERT INTO FACULTY (Name, Department, Designation, Contact, Email) VALUES
('Dr. Robert Johnson', 'Computer Science', 'Professor', '555-0201', 'r.johnson@university.edu'),
('Dr. Lisa Anderson', 'Electronics', 'Associate Professor', '555-0202', 'l.anderson@university.edu'),
('Prof. David Martinez', 'Sports Department', 'Coach', '555-0203', 'd.martinez@university.edu');

-- Insert Sample Equipment
INSERT INTO EQUIPMENT (Name, Category, Purchase_Date, Condition_Status) VALUES
('Dell Laptop i7', 'Laboratory', '2023-01-15', 'Good'),
('Oscilloscope Tektronix', 'Laboratory', '2022-08-20', 'Excellent'),
('Basketball Set', 'Sports', '2023-03-10', 'Good'),
('Guitar Acoustic', 'Music', '2022-11-05', 'Fair'),
('Projector Epson', 'Event Equipment', '2023-06-12', 'Excellent'),
('Microscope Olympus', 'Laboratory', '2021-09-30', 'Good');

-- Insert Sample Locations
INSERT INTO LOCATION (Location_Name, Building, Room_No) VALUES
('Computer Lab 1', 'Engineering Block A', '101'),
('Electronics Lab', 'Engineering Block B', '205'),
('Sports Ground', 'Sports Complex', 'Outdoor'),
('Music Room', 'Arts Building', '305'),
('Auditorium', 'Main Building', 'Ground Floor'),
('Physics Lab', 'Science Block', '402');

-- Insert Sample Usage Records
INSERT INTO EQUIPMENT_USAGE (Equipment_ID, User_ID, User_Type, Location_ID, Date_CheckedOut, Date_Returned) VALUES
(1, 1, 'Student', 1, '2024-01-10', '2024-01-12'),
(3, 3, 'Faculty', 3, '2024-01-15', '2024-01-15'),
(2, 2, 'Student', 2, '2024-01-20', NULL),
(5, 1, 'Faculty', 5, '2024-01-22', '2024-01-23');
