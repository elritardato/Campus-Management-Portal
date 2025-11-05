from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    LOST = "Lost"
    FOUND = "Found"
    CLAIMED = "Claimed"
    RETURNED = "Returned"

class VerificationStatusEnum(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class ItemBase(BaseModel):
    Item_Name: str
    Description: Optional[str] = None
    Category: Optional[str] = None
    Image_Path: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    Item_ID: int
    Date_Reported: datetime

    class Config:
        from_attributes = True

class LostFoundBase(BaseModel):
    Item_ID: int
    Reported_By: int
    Status: StatusEnum = StatusEnum.LOST
    Location: Optional[str] = None

class LostFoundCreate(LostFoundBase):
    pass

class LostFound(LostFoundBase):
    Record_ID: int
    Date_Updated: datetime

    class Config:
        from_attributes = True

class VerificationBase(BaseModel):
    Record_ID: int
    Verified_By: int
    Verification_Status: VerificationStatusEnum = VerificationStatusEnum.PENDING
    Remarks: Optional[str] = None

class VerificationCreate(VerificationBase):
    pass

class Verification(VerificationBase):
    Verification_ID: int
    Verification_Date: datetime

    class Config:
        from_attributes = True