from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional, List
import os
import shutil
from datetime import datetime

from models import ItemCreate, LostFoundCreate, StatusEnum
from schemas import LostFoundResponse, StudentResponse, FacultyResponse
import crud

app = FastAPI(title="Lost and Found API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount uploads directory
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.get("/")
def read_root():
    return {"message": "Lost and Found API is running"}

@app.post("/items/", response_model=dict)
async def create_item_endpoint(
    item_name: str = Form(...),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    reported_by: int = Form(...),
    status: str = Form("Lost"),
    location: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    """Create a new item and lost/found record"""
    
    # Handle image upload
    image_path = None
    if image:
        file_extension = os.path.splitext(image.filename)[1]
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image.filename}"
        image_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    
    # Create item
    item = ItemCreate(
        Item_Name=item_name,
        Description=description,
        Category=category,
        Image_Path=image_path
    )
    item_id = crud.create_item(item)
    
    if not item_id:
        raise HTTPException(status_code=500, detail="Failed to create item")
    
    # Create lost/found record
    lost_found = LostFoundCreate(
        Item_ID=item_id,
        Reported_By=reported_by,
        Status=StatusEnum(status),
        Location=location
    )
    record_id = crud.create_lost_found_record(lost_found)
    
    if not record_id:
        raise HTTPException(status_code=500, detail="Failed to create lost/found record")
    
    return {
        "message": "Item created successfully",
        "item_id": item_id,
        "record_id": record_id
    }

@app.get("/items/", response_model=List[dict])
def get_all_items():
    """Get all lost and found items"""
    return crud.get_all_lost_found_items()

@app.get("/items/status/{status}", response_model=List[dict])
def get_items_by_status(status: str):
    """Get items by status"""
    return crud.get_items_by_status(status)

@app.put("/items/{record_id}/status")
def update_status(record_id: int, new_status: str):
    """Update item status"""
    success = crud.update_item_status(record_id, new_status)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Status updated successfully"}

@app.get("/students/", response_model=List[dict])
def get_students():
    """Get all students"""
    return crud.get_all_students()

@app.get("/faculty/", response_model=List[dict])
def get_faculty():
    """Get all faculty"""
    return crud.get_all_faculty()

@app.get("/search/")
def search_items(q: str):
    """Search items"""
    return crud.search_items(q)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)