import streamlit as st
import requests
import pandas as pd
from datetime import date

# Backend API URL
API_URL = "http://127.0.0.1:8000"

# Page configuration
st.set_page_config(page_title="Equipment Location Tracker", page_icon="📦", layout="wide")

# Sidebar navigation
st.sidebar.title("📦 Equipment Tracker")
page = st.sidebar.radio(
    "Navigate to:",
    ["Dashboard", "Equipment", "Locations", "Students", "Faculty", "Usage"]
)

# Helper function to make API calls
def api_call(method, endpoint, data=None):
    url = f"{API_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

# DASHBOARD PAGE
if page == "Dashboard":
    st.title("📊 Dashboard")
    st.markdown("---")
    
    # Get statistics
    stats = api_call("GET", "/stats")
    
    if stats:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("👨‍🎓 Total Students", stats.get("total_students", 0))
            st.metric("👨‍🏫 Total Faculty", stats.get("total_faculty", 0))
        
        with col2:
            st.metric("📦 Total Equipment", stats.get("total_equipment", 0))
            st.metric("📍 Total Locations", stats.get("total_locations", 0))
        
        with col3:
            st.metric("🔓 Currently Checked Out", stats.get("checked_out", 0))
            st.metric("📝 Total Usage Records", stats.get("total_usage", 0))
    
    st.markdown("---")
    st.subheader("🔓 Currently Checked Out Equipment")
    
    checked_out = api_call("GET", "/usage/checked_out")
    if checked_out:
        if len(checked_out) > 0:
            df = pd.DataFrame(checked_out)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No equipment is currently checked out.")
    
# EQUIPMENT PAGE
elif page == "Equipment":
    st.title("📦 Equipment Management")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["View Equipment", "Add Equipment"])
    
    with tab1:
        st.subheader("All Equipment")
        equipment = api_call("GET", "/equipment")
        
        if equipment:
            if len(equipment) > 0:
                df = pd.DataFrame(equipment)
                st.dataframe(df, use_container_width=True)
                
                # Delete equipment
                st.markdown("#### Delete Equipment")
                eq_id = st.number_input("Enter Equipment ID to delete", min_value=1, step=1, key="del_eq")
                if st.button("Delete Equipment"):
                    result = api_call("DELETE", f"/equipment/{eq_id}")
                    if result:
                        st.success("Equipment deleted successfully!")
                        st.rerun()
            else:
                st.info("No equipment found.")
    
    with tab2:
        st.subheader("Add New Equipment")
        
        with st.form("add_equipment_form"):
            eq_id = st.number_input("Equipment ID", min_value=1, step=1)
            eq_name = st.text_input("Name")
            eq_category = st.selectbox("Category", ["Sports", "Music", "Laboratory", "Event"])
            eq_purchase_date = st.date_input("Purchase Date", value=date.today())
            eq_condition = st.selectbox("Condition Status", ["Excellent", "Good", "Fair", "Poor", "Under Repair"])
            
            submitted = st.form_submit_button("Add Equipment")
            
            if submitted:
                data = {
                    "Equipment_ID": eq_id,
                    "Name": eq_name,
                    "Category": eq_category,
                    "Purchase_Date": str(eq_purchase_date),
                    "Condition_Status": eq_condition
                }
                result = api_call("POST", "/equipment", data)
                if result:
                    st.success("Equipment added successfully!")
                    st.rerun()

# LOCATIONS PAGE
elif page == "Locations":
    st.title("📍 Location Management")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["View Locations", "Add Location"])
    
    with tab1:
        st.subheader("All Locations")
        locations = api_call("GET", "/locations")
        
        if locations:
            if len(locations) > 0:
                df = pd.DataFrame(locations)
                st.dataframe(df, use_container_width=True)
                
                # Delete location
                st.markdown("#### Delete Location")
                loc_id = st.number_input("Enter Location ID to delete", min_value=1, step=1, key="del_loc")
                if st.button("Delete Location"):
                    result = api_call("DELETE", f"/locations/{loc_id}")
                    if result:
                        st.success("Location deleted successfully!")
                        st.rerun()
            else:
                st.info("No locations found.")
    
    with tab2:
        st.subheader("Add New Location")
        
        with st.form("add_location_form"):
            loc_id = st.number_input("Location ID", min_value=1, step=1)
            loc_name = st.text_input("Location Name")
            building = st.text_input("Building")
            room_no = st.text_input("Room Number")
            
            submitted = st.form_submit_button("Add Location")
            
            if submitted:
                data = {
                    "Location_ID": loc_id,
                    "Location_Name": loc_name,
                    "Building": building,
                    "Room_No": room_no
                }
                result = api_call("POST", "/locations", data)
                if result:
                    st.success("Location added successfully!")
                    st.rerun()

# STUDENTS PAGE
elif page == "Students":
    st.title("👨‍🎓 Student Management")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["View Students", "Add Student"])
    
    with tab1:
        st.subheader("All Students")
        students = api_call("GET", "/students")
        
        if students:
            if len(students) > 0:
                df = pd.DataFrame(students)
                st.dataframe(df, use_container_width=True)
                
                # Delete student
                st.markdown("#### Delete Student")
                stud_id = st.number_input("Enter Student ID to delete", min_value=1, step=1, key="del_stud")
                if st.button("Delete Student"):
                    result = api_call("DELETE", f"/students/{stud_id}")
                    if result:
                        st.success("Student deleted successfully!")
                        st.rerun()
            else:
                st.info("No students found.")
    
    with tab2:
        st.subheader("Add New Student")
        
        with st.form("add_student_form"):
            stud_id = st.number_input("Student ID", min_value=1, step=1)
            stud_name = st.text_input("Name")
            department = st.text_input("Department")
            year = st.number_input("Year", min_value=1, max_value=5, step=1)
            contact = st.text_input("Contact")
            email = st.text_input("Email")
            
            submitted = st.form_submit_button("Add Student")
            
            if submitted:
                data = {
                    "Student_ID": stud_id,
                    "Name": stud_name,
                    "Department": department,
                    "Year": year,
                    "Contact": contact,
                    "Email": email
                }
                result = api_call("POST", "/students", data)
                if result:
                    st.success("Student added successfully!")
                    st.rerun()

# FACULTY PAGE
elif page == "Faculty":
    st.title("👨‍🏫 Faculty Management")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["View Faculty", "Add Faculty"])
    
    with tab1:
        st.subheader("All Faculty")
        faculty = api_call("GET", "/faculty")
        
        if faculty:
            if len(faculty) > 0:
                df = pd.DataFrame(faculty)
                st.dataframe(df, use_container_width=True)
                
                # Delete faculty
                st.markdown("#### Delete Faculty")
                fac_id = st.number_input("Enter Faculty ID to delete", min_value=1, step=1, key="del_fac")
                if st.button("Delete Faculty"):
                    result = api_call("DELETE", f"/faculty/{fac_id}")
                    if result:
                        st.success("Faculty deleted successfully!")
                        st.rerun()
            else:
                st.info("No faculty found.")
    
    with tab2:
        st.subheader("Add New Faculty")
        
        with st.form("add_faculty_form"):
            fac_id = st.number_input("Faculty ID", min_value=1, step=1)
            fac_name = st.text_input("Name")
            department = st.text_input("Department")
            designation = st.text_input("Designation")
            contact = st.text_input("Contact")
            email = st.text_input("Email")
            
            submitted = st.form_submit_button("Add Faculty")
            
            if submitted:
                data = {
                    "Faculty_ID": fac_id,
                    "Name": fac_name,
                    "Department": department,
                    "Designation": designation,
                    "Contact": contact,
                    "Email": email
                }
                result = api_call("POST", "/faculty", data)
                if result:
                    st.success("Faculty added successfully!")
                    st.rerun()

# USAGE PAGE
elif page == "Usage":
    st.title("📝 Equipment Usage Management")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["All Usage Records", "Check Out Equipment", "Check In Equipment"])
    
    with tab1:
        st.subheader("All Usage Records")
        usage = api_call("GET", "/usage")
        
        if usage:
            if len(usage) > 0:
                df = pd.DataFrame(usage)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No usage records found.")
    
    with tab2:
        st.subheader("Check Out Equipment")
        
        with st.form("checkout_form"):
            eq_id = st.number_input("Equipment ID", min_value=1, step=1, key="co_eq")
            user_id = st.number_input("User ID", min_value=1, step=1, key="co_user")
            user_type = st.selectbox("User Type", ["Student", "Faculty"])
            loc_id = st.number_input("Location ID", min_value=1, step=1, key="co_loc")
            checkout_date = st.date_input("Check Out Date", value=date.today())
            
            submitted = st.form_submit_button("Check Out")
            
            if submitted:
                data = {
                    "Equipment_ID": eq_id,
                    "User_ID": user_id,
                    "User_Type": user_type,
                    "Location_ID": loc_id,
                    "Date_CheckedOut": str(checkout_date)
                }
                result = api_call("POST", "/check_out", data)
                if result:
                    st.success("Equipment checked out successfully!")
                    st.rerun()
    
    with tab3:
        st.subheader("Check In Equipment")
        
        # Show currently checked out items
        checked_out = api_call("GET", "/usage/checked_out")
        if checked_out and len(checked_out) > 0:
            st.info("Currently Checked Out Equipment:")
            df = pd.DataFrame(checked_out)
            st.dataframe(df, use_container_width=True)
        
        with st.form("checkin_form"):
            usage_id = st.number_input("Usage ID", min_value=1, step=1, key="ci_usage")
            checkin_date = st.date_input("Return Date", value=date.today())
            
            submitted = st.form_submit_button("Check In")
            
            if submitted:
                data = {
                    "Usage_ID": usage_id,
                    "Date_Returned": str(checkin_date)
                }
                result = api_call("POST", "/check_in", data)
                if result:
                    st.success("Equipment checked in successfully!")
                    st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.info("🎓 Equipment Location Tracker\n\nDBMS Project Demo")