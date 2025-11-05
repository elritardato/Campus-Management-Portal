from typing import List, Optional
from database import execute_query
from models import ItemCreate, LostFoundCreate, StatusEnum

def create_item(item: ItemCreate) -> Optional[int]:
    """Create a new item"""
    query = """
        INSERT INTO items (Item_Name, Description, Category, Image_Path)
        VALUES (%s, %s, %s, %s)
    """
    params = (item.Item_Name, item.Description, item.Category, item.Image_Path)
    return execute_query(query, params)

def create_lost_found_record(record: LostFoundCreate) -> Optional[int]:
    """Create a new lost/found record"""
    query = """
        INSERT INTO lost_found (Item_ID, Reported_By, Status, Location)
        VALUES (%s, %s, %s, %s)
    """
    params = (record.Item_ID, record.Reported_By, record.Status.value, record.Location)
    return execute_query(query, params)

def get_all_lost_found_items() -> List[dict]:
    """Get all lost and found items with details"""
    query = """
        SELECT 
            lf.Record_ID,
            lf.Item_ID,
            i.Item_Name,
            i.Description,
            i.Category,
            i.Image_Path,
            lf.Reported_By,
            COALESCE(s.Name, f.Name, 'Unknown') as Reporter_Name,
            lf.Status,
            lf.Location,
            i.Date_Reported,
            lf.Date_Updated
        FROM lost_found lf
        JOIN items i ON lf.Item_ID = i.Item_ID
        LEFT JOIN STUDENTS s ON lf.Reported_By = s.Student_ID
        LEFT JOIN FACULTY f ON lf.Reported_By = f.Faculty_ID
        ORDER BY lf.Date_Updated DESC
    """
    result = execute_query(query, fetch=True)
    return result if result else []

def get_items_by_status(status: str) -> List[dict]:
    """Get items by status"""
    query = """
        SELECT 
            lf.Record_ID,
            lf.Item_ID,
            i.Item_Name,
            i.Description,
            i.Category,
            i.Image_Path,
            lf.Reported_By,
            COALESCE(s.Name, f.Name, 'Unknown') as Reporter_Name,
            lf.Status,
            lf.Location,
            i.Date_Reported,
            lf.Date_Updated
        FROM lost_found lf
        JOIN items i ON lf.Item_ID = i.Item_ID
        LEFT JOIN STUDENTS s ON lf.Reported_By = s.Student_ID
        LEFT JOIN FACULTY f ON lf.Reported_By = f.Faculty_ID
        WHERE lf.Status = %s
        ORDER BY lf.Date_Updated DESC
    """
    result = execute_query(query, (status,), fetch=True)
    return result if result else []

def update_item_status(record_id: int, new_status: str) -> bool:
    """Update the status of a lost/found item"""
    query = """
        UPDATE lost_found 
        SET Status = %s 
        WHERE Record_ID = %s
    """
    result = execute_query(query, (new_status, record_id))
    return result is not None

def get_all_students() -> List[dict]:
    """Get all students"""
    query = "SELECT * FROM STUDENTS ORDER BY Name"
    result = execute_query(query, fetch=True)
    return result if result else []

def get_all_faculty() -> List[dict]:
    """Get all faculty"""
    query = "SELECT * FROM FACULTY ORDER BY Name"
    result = execute_query(query, fetch=True)
    return result if result else []

def search_items(search_term: str) -> List[dict]:
    """Search items by name, description, or category"""
    query = """
        SELECT 
            lf.Record_ID,
            lf.Item_ID,
            i.Item_Name,
            i.Description,
            i.Category,
            i.Image_Path,
            lf.Reported_By,
            COALESCE(s.Name, f.Name, 'Unknown') as Reporter_Name,
            lf.Status,
            lf.Location,
            i.Date_Reported,
            lf.Date_Updated
        FROM lost_found lf
        JOIN items i ON lf.Item_ID = i.Item_ID
        LEFT JOIN STUDENTS s ON lf.Reported_By = s.Student_ID
        LEFT JOIN FACULTY f ON lf.Reported_By = f.Faculty_ID
        WHERE i.Item_Name LIKE %s 
           OR i.Description LIKE %s 
           OR i.Category LIKE %s
        ORDER BY lf.Date_Updated DESC
    """
    search_pattern = f"%{search_term}%"
    result = execute_query(query, (search_pattern, search_pattern, search_pattern), fetch=True)
    return result if result else []