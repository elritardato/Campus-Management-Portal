import streamlit as st
import requests
from datetime import datetime
import os
from PIL import Image

# Configure page
st.set_page_config(
    page_title="Campus Lost & Found",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern college-style UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #4F46E5;
        --secondary-color: #10B981;
        --accent-color: #F59E0B;
        --danger-color: #EF4444;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Modern card styling */
    .stCard {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: white;
        margin-bottom: 1rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* Item card styling */
    .item-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 4px solid #4F46E5;
    }
    
    .item-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
    }
    
    .status-lost {
        background-color: #FEE2E2;
        color: #991B1B;
    }
    
    .status-found {
        background-color: #D1FAE5;
        color: #065F46;
    }
    
    .status-claimed {
        background-color: #DBEAFE;
        color: #1E40AF;
    }
    
    .status-returned {
        background-color: #E0E7FF;
        color: #3730A3;
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
    }
    
    .stats-label {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: transform 0.2s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #F9FAFB;
    }
    
    /* Form styling */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 2px solid #E5E7EB;
        padding: 0.75rem;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# API Base URL
API_URL = "http://localhost:8000"

# Helper functions
def get_all_items():
    try:
        response = requests.get(f"{API_URL}/items/")
        return response.json() if response.status_code == 200 else []
    except:
        return []

def get_students():
    try:
        response = requests.get(f"{API_URL}/students/")
        return response.json() if response.status_code == 200 else []
    except:
        return []

def get_faculty():
    try:
        response = requests.get(f"{API_URL}/faculty/")
        return response.json() if response.status_code == 200 else []
    except:
        return []

def create_item(data, image_file):
    try:
        files = {"image": image_file} if image_file else {}
        response = requests.post(f"{API_URL}/items/", data=data, files=files)
        return response.status_code == 200
    except:
        return False

def update_status(record_id, new_status):
    try:
        response = requests.put(f"{API_URL}/items/{record_id}/status", params={"new_status": new_status})
        return response.status_code == 200
    except:
        return False

def search_items(query):
    try:
        response = requests.get(f"{API_URL}/search/", params={"q": query})
        return response.json() if response.status_code == 200 else []
    except:
        return []

# Main header
st.markdown("""
<div class="main-header">
    <h1>🎓 Campus Lost & Found</h1>
    <p>Your trusted platform for recovering lost items on campus</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/search.png", width=80)
    st.title("Navigation")
    page = st.radio("", ["📋 Dashboard", "➕ Report Item", "🔍 Search Items", "📊 Statistics"])
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    items = get_all_items()
    lost_count = len([i for i in items if i['Status'] == 'Lost'])
    found_count = len([i for i in items if i['Status'] == 'Found'])
    
    st.metric("Lost Items", lost_count, delta=None)
    st.metric("Found Items", found_count, delta=None)

# Dashboard Page
if page == "📋 Dashboard":
    st.header("📋 All Items")
    
    # Filter options
    col1, col2 = st.columns([3, 1])
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Lost", "Found", "Claimed", "Returned"])
    
    items = get_all_items()
    
    if status_filter != "All":
        items = [item for item in items if item['Status'] == status_filter]
    
    if not items:
        st.info("No items found. Start by reporting a lost or found item!")
    else:
        # Display items in a grid
        for item in items:
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 1])
                
                with col1:
                    if item.get('Image_Path'):
                        try:
                            st.image(f"{API_URL}/{item['Image_Path']}", width=120)
                        except:
                            st.image("https://via.placeholder.com/120", width=120)
                    else:
                        st.image("https://via.placeholder.com/120", width=120)
                
                with col2:
                    st.markdown(f"### {item['Item_Name']}")
                    st.markdown(f"**Category:** {item.get('Category', 'N/A')}")
                    st.markdown(f"**Description:** {item.get('Description', 'No description')}")
                    st.markdown(f"**Location:** {item.get('Location', 'Not specified')}")
                    st.markdown(f"**Reported by:** {item.get('Reporter_Name', 'Unknown')}")
                    st.markdown(f"**Date:** {item.get('Date_Reported', 'N/A')}")
                
                with col3:
                    status_class = f"status-{item['Status'].lower()}"
                    st.markdown(f'<div class="status-badge {status_class}">{item["Status"]}</div>', unsafe_allow_html=True)
                    
                    st.markdown("---")
                    new_status = st.selectbox(
                        "Update Status",
                        ["Lost", "Found", "Claimed", "Returned"],
                        key=f"status_{item['Record_ID']}",
                        index=["Lost", "Found", "Claimed", "Returned"].index(item['Status'])
                    )
                    
                    if st.button("Update", key=f"update_{item['Record_ID']}"):
                        if update_status(item['Record_ID'], new_status):
                            st.success("Status updated!")
                            st.rerun()
                        else:
                            st.error("Failed to update status")
                
                st.markdown("---")

# Report Item Page
elif page == "➕ Report Item":
    st.header("➕ Report Lost or Found Item")
    
    with st.form("report_item_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            item_name = st.text_input("Item Name *", placeholder="e.g., Blue Backpack")
            category = st.selectbox("Category", ["Electronics", "Books", "Clothing", "Accessories", "Documents", "Other"])
            status = st.selectbox("Status *", ["Lost", "Found"])
            location = st.text_input("Location", placeholder="e.g., Library, 2nd Floor")
        
        with col2:
            description = st.text_area("Description", placeholder="Provide detailed description...", height=100)
            
            # Get reporters
            students = get_students()
            faculty = get_faculty()
            
            reporter_options = {}
            if students:
                for s in students:
                    reporter_options[f"Student - {s['Name']} ({s['Student_ID']})"] = s['Student_ID']
            if faculty:
                for f in faculty:
                    reporter_options[f"Faculty - {f['Name']} ({f['Faculty_ID']})"] = f['Faculty_ID']
            
            selected_reporter = st.selectbox("Reported By *", list(reporter_options.keys()) if reporter_options else ["No users found"])
            
            image = st.file_uploader("Upload Image (Optional)", type=["jpg", "jpeg", "png"])
        
        submitted = st.form_submit_button("🚀 Submit Report", use_container_width=True)
        
        if submitted:
            if not item_name or not selected_reporter:
                st.error("Please fill in all required fields marked with *")
            elif selected_reporter == "No users found":
                st.error("No students or faculty found in database. Please add users first.")
            else:
                data = {
                    "item_name": item_name,
                    "description": description,
                    "category": category,
                    "reported_by": reporter_options[selected_reporter],
                    "status": status,
                    "location": location
                }
                
                if create_item(data, image):
                    st.success("✅ Item reported successfully!")
                    st.balloons()
                else:
                    st.error("❌ Failed to report item. Please try again.")

# Search Items Page
elif page == "🔍 Search Items":
    st.header("🔍 Search Items")
    
    search_query = st.text_input("Search by name, description, or category", placeholder="Type to search...")
    
    if search_query:
        results = search_items(search_query)
        
        if not results:
            st.info("No items found matching your search.")
        else:
            st.success(f"Found {len(results)} item(s)")
            
            for item in results:
                with st.container():
                    col1, col2, col3 = st.columns([1, 3, 1])
                    
                    with col1:
                        if item.get('Image_Path'):
                            try:
                                st.image(f"{API_URL}/{item['Image_Path']}", width=120)
                            except:
                                st.image("https://via.placeholder.com/120", width=120)
                        else:
                            st.image("https://via.placeholder.com/120", width=120)
                    
                    with col2:
                        st.markdown(f"### {item['Item_Name']}")
                        st.markdown(f"**Category:** {item.get('Category', 'N/A')}")
                        st.markdown(f"**Description:** {item.get('Description', 'No description')}")
                        st.markdown(f"**Location:** {item.get('Location', 'Not specified')}")
                    
                    with col3:
                        status_class = f"status-{item['Status'].lower()}"
                        st.markdown(f'<div class="status-badge {status_class}">{item["Status"]}</div>', unsafe_allow_html=True)
                    
                    st.markdown("---")

# Statistics Page
elif page == "📊 Statistics":
    st.header("📊 Statistics Dashboard")
    
    items = get_all_items()
    
    # Overview stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <p class="stats-number">{len(items)}</p>
            <p class="stats-label">Total Items</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        lost = len([i for i in items if i['Status'] == 'Lost'])
        st.markdown(f"""
        <div class="stats-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <p class="stats-number">{lost}</p>
            <p class="stats-label">Lost Items</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        found = len([i for i in items if i['Status'] == 'Found'])
        st.markdown(f"""
        <div class="stats-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <p class="stats-number">{found}</p>
            <p class="stats-label">Found Items</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        returned = len([i for i in items if i['Status'] == 'Returned'])
        st.markdown(f"""
        <div class="stats-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <p class="stats-number">{returned}</p>
            <p class="stats-label">Returned Items</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Category breakdown
    st.subheader("📂 Items by Category")
    
    if items:
        from collections import Counter
        categories = Counter([item.get('Category', 'Unknown') for item in items])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create a simple bar chart using streamlit
            import pandas as pd
            df = pd.DataFrame(list(categories.items()), columns=['Category', 'Count'])
            st.bar_chart(df.set_index('Category'))
        
        with col2:
            st.markdown("### Category Summary")
            for category, count in categories.most_common():
                percentage = (count / len(items)) * 100
                st.markdown(f"**{category}:** {count} ({percentage:.1f}%)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    recent_items = sorted(items, key=lambda x: x.get('Date_Updated', ''), reverse=True)[:5]
    
    for item in recent_items:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**{item['Item_Name']}** - {item.get('Category', 'N/A')}")
        
        with col2:
            status_class = f"status-{item['Status'].lower()}"
            st.markdown(f'<div class="status-badge {status_class}">{item["Status"]}</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"*{item.get('Date_Updated', 'N/A')}*")
        
        st.markdown("---")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #6B7280;">
    <p>🎓 Campus Lost & Found System | Made with ❤️ for Students</p>
    <p style="font-size: 0.9rem;">Contact Admin: admin@campus.edu | Emergency: 1800-XXX-XXXX</p>
</div>
""", unsafe_allow_html=True)
            