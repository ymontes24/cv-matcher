from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class DocumentBase(BaseModel):
    title: str
    content: str
    
class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        orm_mode = True

class CVCreate(DocumentCreate):
    candidate_name: str
    
class CV(Document):
    candidate_name: str

class DocumentResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    
    class Config:
        orm_mode = True

class CVResponse(DocumentResponse):
    candidate_name: str
