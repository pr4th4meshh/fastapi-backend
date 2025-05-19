from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    role: str = Field(default="volunteer", pattern="^(admin|volunteer|team-member)$")
    avatar: Optional[str] = None
    location: Optional[str] = None
    workTypePreference: Optional[str] = None
    gender: Optional[str] = None
    causePreference: Optional[str] = None
    organizationName: Optional[str] = None
    warnings: int = 0
    isBanned: bool = False
    banReason: Optional[str] = None
    lastWarningDate: Optional[datetime] = None
    
    
class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True