-- Create and use database
CREATE DATABASE IF NOT EXISTS lost_found_db;
USE lost_found_db;

-- Drop tables if they exist (be careful with this!)
DROP TABLE IF EXISTS verification;
DROP TABLE IF EXISTS lost_found;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS FACULTY;
DROP TABLE IF EXISTS STUDENTS;

-- Create STUDENTS table
CREATE TABLE STUDENTS (
    Student_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Department VARCHAR(100),
    Year INT,
    Contact VARCHAR(15),
    Email VARCHAR(100)
);

-- Create FACULTY table
CREATE TABLE FACULTY (
    Faculty_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Department VARCHAR(100),
    Designation VARCHAR(100),
    Contact VARCHAR(15),
    Email VARCHAR(100)
);

-- Create ITEMS table
CREATE TABLE items (
    Item_ID INT PRIMARY KEY AUTO_INCREMENT,
    Item_Name VARCHAR(100) NOT NULL,
    Description TEXT,
    Category VARCHAR(50),
    Image_Path VARCHAR(255),
    Date_Reported TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create LOST_FOUND table
CREATE TABLE lost_found (
    Record_ID INT PRIMARY KEY AUTO_INCREMENT,
    Item_ID INT NOT NULL,
    Reported_By INT NOT NULL,
    Status ENUM('Lost', 'Found', 'Claimed', 'Returned') DEFAULT 'Lost',
    Location VARCHAR(200),
    Date_Updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (Item_ID) REFERENCES items(Item_ID) ON DELETE CASCADE
);

-- Create VERIFICATION table
CREATE TABLE verification (
    Verification_ID INT PRIMARY KEY AUTO_INCREMENT,
    Record_ID INT NOT NULL,
    Verified_By INT NOT NULL,
    Verification_Status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    Remarks TEXT,
    Verification_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Record_ID) REFERENCES lost_found(Record_ID) ON DELETE CASCADE
);

-- Insert Sample Students
INSERT INTO STUDENTS (Student_ID, Name, Department, Year, Contact, Email) VALUES
(1001, 'Raj Kale', 'Computer Science', 3, '9876543210', 'raj@campus.edu'),
(1002, 'Abhimanyu Kadhane', 'Electronics', 2, '9876543211', 'abhimanyu@campus.edu'),
(1003, 'Vandan Jethwa', 'Mechanical', 4, '9876543212', 'vandan@campus.edu'),
(1004, 'Yukino Yukinoshita', 'Information Technology', 2, '9876543213', 'yukinon@campus.edu'),
(1005, 'Furina', 'Civil', 3, '9876543214', 'furina@campus.edu');

-- Insert Sample Faculty
INSERT INTO FACULTY (Faculty_ID, Name, Department, Designation, Contact, Email) VALUES
(2001, 'NAB Sir', 'Computer Science', 'Professor', '9876543220', 'anjali@campus.edu'),
(2002, 'Prof. Anand Godbole', 'Electronics', 'Associate Professor', '9876543221', 'rajesh@campus.edu'),
(2003, 'Prof. Pramod Bide', 'Mechanical', 'Assistant Professor', '9876543222', 'sunita@campus.edu');

-- Show what we created
SHOW TABLES;
SELECT 'Students:' as '';
SELECT * FROM STUDENTS;
SELECT 'Faculty:' as '';
SELECT * FROM FACULTY;
