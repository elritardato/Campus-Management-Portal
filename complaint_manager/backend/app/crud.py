from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from backend.app import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_category(db: Session, category: schemas.ComplaintCategoryCreate):
    db_category = models.ComplaintCategory(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ComplaintCategory).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    return db.query(models.ComplaintCategory).filter(models.ComplaintCategory.id == category_id).first()

def create_complaint(db: Session, complaint: schemas.ComplaintCreate):
    db_complaint = models.Complaint(**complaint.model_dump())
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

def get_complaints(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None, category_id: Optional[int] = None):
    query = db.query(models.Complaint)
    if status:
        query = query.filter(models.Complaint.status == status)
    if category_id:
        query = query.filter(models.Complaint.category_id == category_id)
    return query.offset(skip).limit(limit).all()

def get_complaint(db: Session, complaint_id: int):
    return db.query(models.Complaint).filter(models.Complaint.id == complaint_id).first()

def update_complaint(db: Session, complaint_id: int, complaint_update: schemas.ComplaintUpdate):
    db_complaint = get_complaint(db, complaint_id)
    if db_complaint:
        update_data = complaint_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_complaint, key, value)
        db.commit()
        db.refresh(db_complaint)
    return db_complaint

def create_comment(db: Session, comment: schemas.ComplaintCommentCreate):
    db_comment = models.ComplaintComment(**comment.model_dump())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_complaint_comments(db: Session, complaint_id: int):
    return db.query(models.ComplaintComment).filter(models.ComplaintComment.complaint_id == complaint_id).all()

def create_status_history(db: Session, status_history: schemas.ComplaintStatusHistoryCreate):
    db_history = models.ComplaintStatusHistory(**status_history.model_dump())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

def get_complaint_status_history(db: Session, complaint_id: int):
    return db.query(models.ComplaintStatusHistory).filter(models.ComplaintStatusHistory.complaint_id == complaint_id).all()

def create_attachment(db: Session, attachment: schemas.ComplaintAttachmentCreate):
    db_attachment = models.ComplaintAttachment(**attachment.model_dump())
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

def get_complaint_attachments(db: Session, complaint_id: int):
    return db.query(models.ComplaintAttachment).filter(models.ComplaintAttachment.complaint_id == complaint_id).all()
