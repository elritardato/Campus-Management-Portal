from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app import schemas, crud
from backend.app.database import get_db

router = APIRouter(prefix="/api/v1/complaints", tags=["complaints"])

@router.post("/", response_model=schemas.Complaint)
def create_complaint(complaint: schemas.ComplaintCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=complaint.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_category = crud.get_category(db, category_id=complaint.category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return crud.create_complaint(db=db, complaint=complaint)

@router.get("/", response_model=List[schemas.Complaint])
def read_complaints(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[str] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    complaints = crud.get_complaints(db, skip=skip, limit=limit, status=status, category_id=category_id)
    return complaints

@router.get("/{complaint_id}", response_model=schemas.Complaint)
def read_complaint(complaint_id: int, db: Session = Depends(get_db)):
    db_complaint = crud.get_complaint(db, complaint_id=complaint_id)
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return db_complaint

@router.patch("/{complaint_id}", response_model=schemas.Complaint)
def update_complaint(
    complaint_id: int, 
    complaint_update: schemas.ComplaintUpdate, 
    db: Session = Depends(get_db)
):
    db_complaint = crud.update_complaint(db, complaint_id=complaint_id, complaint_update=complaint_update)
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return db_complaint

@router.post("/{complaint_id}/comments", response_model=schemas.ComplaintComment)
def create_complaint_comment(
    complaint_id: int,
    comment: schemas.ComplaintCommentBase,
    user_id: int,
    db: Session = Depends(get_db)
):
    db_complaint = crud.get_complaint(db, complaint_id=complaint_id)
    if not db_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    comment_create = schemas.ComplaintCommentCreate(
        complaint_id=complaint_id,
        user_id=user_id,
        comment=comment.comment
    )
    return crud.create_comment(db=db, comment=comment_create)

@router.get("/{complaint_id}/comments", response_model=List[schemas.ComplaintComment])
def read_complaint_comments(complaint_id: int, db: Session = Depends(get_db)):
    return crud.get_complaint_comments(db, complaint_id=complaint_id)

@router.post("/{complaint_id}/status", response_model=schemas.ComplaintStatusHistory)
def update_complaint_status(
    complaint_id: int,
    status_update: schemas.ComplaintStatusHistoryBase,
    changed_by: int,
    db: Session = Depends(get_db)
):
    db_complaint = crud.get_complaint(db, complaint_id=complaint_id)
    if not db_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    old_status = db_complaint.status
    db_complaint.status = status_update.new_status
    db.commit()
    
    status_history = schemas.ComplaintStatusHistoryCreate(
        complaint_id=complaint_id,
        old_status=old_status,
        new_status=status_update.new_status,
        changed_by=changed_by,
        remark=status_update.remark
    )
    return crud.create_status_history(db=db, status_history=status_history)

@router.get("/{complaint_id}/status-history", response_model=List[schemas.ComplaintStatusHistory])
def read_complaint_status_history(complaint_id: int, db: Session = Depends(get_db)):
    return crud.get_complaint_status_history(db, complaint_id=complaint_id)

@router.post("/{complaint_id}/attachments", response_model=schemas.ComplaintAttachment)
def create_complaint_attachment(
    complaint_id: int,
    attachment: schemas.ComplaintAttachmentBase,
    uploaded_by: int,
    db: Session = Depends(get_db)
):
    db_complaint = crud.get_complaint(db, complaint_id=complaint_id)
    if not db_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    attachment_create = schemas.ComplaintAttachmentCreate(
        complaint_id=complaint_id,
        uploaded_by=uploaded_by,
        **attachment.model_dump()
    )
    return crud.create_attachment(db=db, attachment=attachment_create)

@router.get("/{complaint_id}/attachments", response_model=List[schemas.ComplaintAttachment])
def read_complaint_attachments(complaint_id: int, db: Session = Depends(get_db)):
    return crud.get_complaint_attachments(db, complaint_id=complaint_id)
