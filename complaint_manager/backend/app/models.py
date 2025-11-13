from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    complaints = relationship("Complaint", back_populates="user", foreign_keys="Complaint.user_id")
    assigned_complaints = relationship("Complaint", back_populates="assigned_user", foreign_keys="Complaint.assigned_to")
    comments = relationship("ComplaintComment", back_populates="user")

class ComplaintCategory(Base):
    __tablename__ = "complaint_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    
    complaints = relationship("Complaint", back_populates="category")

class Complaint(Base):
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("complaint_categories.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="open")
    assigned_to = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="complaints", foreign_keys=[user_id])
    assigned_user = relationship("User", back_populates="assigned_complaints", foreign_keys=[assigned_to])
    category = relationship("ComplaintCategory", back_populates="complaints")
    comments = relationship("ComplaintComment", back_populates="complaint", cascade="all, delete-orphan")
    status_history = relationship("ComplaintStatusHistory", back_populates="complaint", cascade="all, delete-orphan")
    attachments = relationship("ComplaintAttachment", back_populates="complaint", cascade="all, delete-orphan")

class ComplaintComment(Base):
    __tablename__ = "complaint_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    complaint = relationship("Complaint", back_populates="comments")
    user = relationship("User", back_populates="comments")

class ComplaintStatusHistory(Base):
    __tablename__ = "complaint_status_history"
    
    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id", ondelete="CASCADE"), nullable=False)
    old_status = Column(String(50))
    new_status = Column(String(50), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    remark = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    
    complaint = relationship("Complaint", back_populates="status_history")

class ComplaintAttachment(Base):
    __tablename__ = "complaint_attachments"
    
    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(100))
    uploaded_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    complaint = relationship("Complaint", back_populates="attachments")