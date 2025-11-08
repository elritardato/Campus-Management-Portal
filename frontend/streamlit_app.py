import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Complaint Management System", layout="wide")

def get_users():
    response = requests.get(f"{API_BASE_URL}/api/v1/users")
    return response.json() if response.status_code == 200 else []

def get_categories():
    response = requests.get(f"{API_BASE_URL}/api/v1/categories")
    return response.json() if response.status_code == 200 else []

def get_complaints(status=None, category_id=None):
    params = {}
    if status:
        params["status"] = status
    if category_id:
        params["category_id"] = category_id
    response = requests.get(f"{API_BASE_URL}/api/v1/complaints", params=params)
    return response.json() if response.status_code == 200 else []

def create_complaint(user_id, category_id, title, description):
    data = {
        "user_id": user_id,
        "category_id": category_id,
        "title": title,
        "description": description
    }
    response = requests.post(f"{API_BASE_URL}/api/v1/complaints", json=data)
    return response.json() if response.status_code == 200 else None

def add_comment(complaint_id, user_id, comment):
    response = requests.post(
        f"{API_BASE_URL}/api/v1/complaints/{complaint_id}/comments",
        params={"user_id": user_id},
        json={"comment": comment}
    )
    return response.json() if response.status_code == 200 else None

def update_status(complaint_id, new_status, changed_by, remark=""):
    response = requests.post(
        f"{API_BASE_URL}/api/v1/complaints/{complaint_id}/status",
        params={"changed_by": changed_by},
        json={"new_status": new_status, "remark": remark}
    )
    return response.json() if response.status_code == 200 else None

def get_complaint_comments(complaint_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/complaints/{complaint_id}/comments")
    return response.json() if response.status_code == 200 else []

st.title("Complaint Management System")

users = get_users()
categories = get_categories()

if not users:
    st.error("Unable to connect to the backend API. Please ensure the backend is running.")
    st.stop()

user_options = {f"{u['full_name']} ({u['email']})": u['id'] for u in users}
selected_user = st.sidebar.selectbox("Select User", list(user_options.keys()))
current_user_id = user_options[selected_user]
current_user = next((u for u in users if u['id'] == current_user_id), None)

st.sidebar.markdown(f"**Role:** {current_user['role'] if current_user else 'N/A'}")
st.sidebar.markdown("---")

menu = st.sidebar.radio("Menu", ["View Complaints", "Create Complaint", "My Complaints"])

if menu == "Create Complaint":
    st.header("Create New Complaint")
    
    with st.form("create_complaint_form"):
        title = st.text_input("Complaint Title")
        category_id = st.selectbox(
            "Category",
            options=[c['id'] for c in categories],
            format_func=lambda x: next((c['name'] for c in categories if c['id'] == x), "")
        )
        description = st.text_area("Description")
        
        submitted = st.form_submit_button("Submit Complaint")
        
        if submitted:
            if title and description:
                result = create_complaint(current_user_id, category_id, title, description)
                if result:
                    st.success(f"Complaint created successfully! ID: {result['id']}")
                else:
                    st.error("Failed to create complaint")
            else:
                st.warning("Please fill in all fields")

elif menu == "View Complaints":
    st.header("All Complaints")
    
    col1, col2 = st.columns(2)
    with col1:
        filter_status = st.selectbox("Filter by Status", ["All", "open", "in_progress", "resolved", "closed"])
    with col2:
        filter_category = st.selectbox(
            "Filter by Category",
            ["All"] + [c['name'] for c in categories]
        )
    
    status_param = None if filter_status == "All" else filter_status
    category_param = None
    if filter_category != "All":
        category_param = next((c['id'] for c in categories if c['name'] == filter_category), None)
    
    complaints = get_complaints(status=status_param, category_id=category_param)
    
    if complaints:
        for complaint in complaints:
            with st.expander(f"#{complaint['id']} - {complaint['title']} [{complaint['status']}]"):
                st.markdown(f"**Description:** {complaint['description']}")
                
                user = next((u for u in users if u['id'] == complaint['user_id']), None)
                category = next((c for c in categories if c['id'] == complaint['category_id']), None)
                
                st.markdown(f"**Submitted by:** {user['full_name'] if user else 'Unknown'}")
                st.markdown(f"**Category:** {category['name'] if category else 'Unknown'}")
                st.markdown(f"**Created:** {complaint['created_at']}")
                st.markdown(f"**Last Updated:** {complaint['updated_at']}")
                
                if complaint.get('assigned_to'):
                    assigned = next((u for u in users if u['id'] == complaint['assigned_to']), None)
                    st.markdown(f"**Assigned to:** {assigned['full_name'] if assigned else 'Unknown'}")
                
                st.markdown("---")
                st.subheader("Comments")
                comments = get_complaint_comments(complaint['id'])
                if comments:
                    for comment in comments:
                        comment_user = next((u for u in users if u['id'] == comment['user_id']), None)
                        st.markdown(f"**{comment_user['full_name'] if comment_user else 'Unknown'}** - {comment['created_at']}")
                        st.markdown(f"> {comment['comment']}")
                else:
                    st.info("No comments yet")
                
                st.markdown("---")
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    new_comment = st.text_input(f"Add comment to complaint #{complaint['id']}", key=f"comment_{complaint['id']}")
                    if st.button("Add Comment", key=f"btn_comment_{complaint['id']}"):
                        if new_comment:
                            result = add_comment(complaint['id'], current_user_id, new_comment)
                            if result:
                                st.success("Comment added!")
                                st.rerun()
                
                if current_user and current_user['role'] == 'admin':
                    with col2:
                        new_status = st.selectbox(
                            "Update Status",
                            ["open", "in_progress", "resolved", "closed"],
                            key=f"status_{complaint['id']}"
                        )
                        if st.button("Update", key=f"btn_status_{complaint['id']}"):
                            result = update_status(complaint['id'], new_status, current_user_id, "Status updated via admin panel")
                            if result:
                                st.success("Status updated!")
                                st.rerun()
    else:
        st.info("No complaints found")

elif menu == "My Complaints":
    st.header("My Complaints")
    
    all_complaints = get_complaints()
    my_complaints = [c for c in all_complaints if c['user_id'] == current_user_id]
    
    if my_complaints:
        for complaint in my_complaints:
            with st.expander(f"#{complaint['id']} - {complaint['title']} [{complaint['status']}]"):
                st.markdown(f"**Description:** {complaint['description']}")
                
                category = next((c for c in categories if c['id'] == complaint['category_id']), None)
                st.markdown(f"**Category:** {category['name'] if category else 'Unknown'}")
                st.markdown(f"**Status:** {complaint['status']}")
                st.markdown(f"**Created:** {complaint['created_at']}")
                st.markdown(f"**Last Updated:** {complaint['updated_at']}")
                
                if complaint.get('assigned_to'):
                    assigned = next((u for u in users if u['id'] == complaint['assigned_to']), None)
                    st.markdown(f"**Assigned to:** {assigned['full_name'] if assigned else 'Unknown'}")
                
                st.markdown("---")
                st.subheader("Comments")
                comments = get_complaint_comments(complaint['id'])
                if comments:
                    for comment in comments:
                        comment_user = next((u for u in users if u['id'] == comment['user_id']), None)
                        st.markdown(f"**{comment_user['full_name'] if comment_user else 'Unknown'}** - {comment['created_at']}")
                        st.markdown(f"> {comment['comment']}")
                else:
                    st.info("No comments yet")
                
                st.markdown("---")
                new_comment = st.text_input(f"Add comment", key=f"my_comment_{complaint['id']}")
                if st.button("Add Comment", key=f"my_btn_{complaint['id']}"):
                    if new_comment:
                        result = add_comment(complaint['id'], current_user_id, new_comment)
                        if result:
                            st.success("Comment added!")
                            st.rerun()
    else:
        st.info("You haven't submitted any complaints yet")

st.sidebar.markdown("---")
st.sidebar.markdown("### System Status")
try:
    health = requests.get(f"{API_BASE_URL}/health", timeout=2)
    if health.status_code == 200:
        st.sidebar.success("Backend: Online")
    else:
        st.sidebar.error("Backend: Error")
except:
    st.sidebar.error("Backend: Offline")
