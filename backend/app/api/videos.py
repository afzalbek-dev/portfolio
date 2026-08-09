from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.models import Project
from app.schemas.schemas import ProjectResponse

router = APIRouter(tags=["Video Projects"])

@router.get("/videos", response_model=List[ProjectResponse])
def get_video_projects(db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.category == "ai_video", Project.is_published == True).order_by(Project.order_index).all()
