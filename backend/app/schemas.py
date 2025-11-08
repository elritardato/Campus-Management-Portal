from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ComplaintCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class ComplaintCategoryCreate(ComplaintCategoryBase):
    pass

class ComplaintCategory(ComplaintCategoryBase):
    id: int
    
    class Config:
        from_attributes = True

class ComplaintBase(BaseModel):
    title: str
    description: Optional[str] = None
    category_id: int

class ComplaintCreate(ComplaintBase):
    user_id: int

class ComplaintUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[int] = None

class Complaint(ComplaintBase):
    id: int
    user_id: int
    status: str
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ComplaintCommentBase(BaseModel):
    comment: str

class ComplaintCommentCreate(ComplaintCommentBase):
    complaint_id: int
    user_id: int

class ComplaintComment(ComplaintCommentBase):
    id: int
    complaint_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ComplaintStatusHistoryBase(BaseModel):
    new_status: str
    remark: Optional[str] = None

class ComplaintStatusHistoryCreate(ComplaintStatusHistoryBase):
    complaint_id: int
    old_status: Optional[str] = None
    changed_by: int

class ComplaintStatusHistory(ComplaintStatusHistoryBase):
    id: int
    complaint_id: int
    old_status: Optional[str] = None
    changed_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ComplaintAttachmentBase(BaseModel):
    file_name: str
    file_path: str
    file_type: Optional[str] = None

class ComplaintAttachmentCreate(ComplaintAttachmentBase):
    complaint_id: int
    uploaded_by: int

class ComplaintAttachment(ComplaintAttachmentBase):
    id: int
    complaint_id: int
    uploaded_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True
