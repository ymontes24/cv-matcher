from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class DocumentBase(BaseModel):
    job_title: str
    job_description: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True

class JobDescriptionCreate(DocumentCreate):
    company_name: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None

class JobDescription(Document):
    company_name: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None

class DocumentResponse(BaseModel):
    id: str
    job_title: str
    job_description: str
    created_at: datetime

    class Config:
        orm_mode = True

class JobDescriptionResponse(DocumentResponse):
    company_name: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    