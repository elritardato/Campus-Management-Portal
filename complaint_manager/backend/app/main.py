from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app import models, crud, schemas
from app.routers import users, categories, complaints
import sys


app = FastAPI(title="Complaint Management System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(complaints.router)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    seed_initial_data()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Complaint Management System API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

def seed_initial_data():
    db = SessionLocal()
    try:
        existing_users = db.query(models.User).first()
        if existing_users:
            return
        
        users_data = [
            {"full_name": "Admin User", "email": "admin@example.com", "role": "admin"},
            {"full_name": "John Doe", "email": "john@example.com", "role": "user"},
            {"full_name": "Jane Smith", "email": "jane@example.com", "role": "user"},
            {"full_name": "Support Team", "email": "support@example.com", "role": "admin"},
        ]
        
        for user_data in users_data:
            user = schemas.UserCreate(**user_data)
            crud.create_user(db, user)
        
        categories_data = [
            {"name": "Technical", "description": "Technical issues and bugs"},
            {"name": "Billing", "description": "Billing and payment related issues"},
            {"name": "Service", "description": "Service quality and delivery issues"},
            {"name": "General", "description": "General inquiries and feedback"},
        ]
        
        for category_data in categories_data:
            category = schemas.ComplaintCategoryCreate(**category_data)
            crud.create_category(db, category)
        
        complaints_data = [
            {
                "user_id": 2,
                "category_id": 1,
                "title": "Website not loading",
                "description": "The website takes too long to load and sometimes times out"
            },
            {
                "user_id": 3,
                "category_id": 2,
                "title": "Incorrect billing amount",
                "description": "I was charged twice for my last order"
            },
        ]
        
        for complaint_data in complaints_data:
            complaint = schemas.ComplaintCreate(**complaint_data)
            crud.create_complaint(db, complaint)
        
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    if "--init-db" in sys.argv:
        Base.metadata.create_all(bind=engine)
        seed_initial_data()
        print("Database initialized and seeded!")
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)
