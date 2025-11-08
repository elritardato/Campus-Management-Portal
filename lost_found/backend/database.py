import pymysql
from pymysql import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'dashboard_user'),
            password=os.getenv('DB_PASSWORD', 'StrongPass123!'),
            database=os.getenv('DB_NAME', 'lost_found_db'),
            port=int(os.getenv('DB_PORT', 3306)),
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    """Execute a query and return results if fetch=True"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        else:
            connection.commit()
            last_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return last_id
    except Error as e:
        print(f"Error executing query: {e}")
        if connection:
            connection.close()
        return None