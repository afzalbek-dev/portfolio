from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.models import Project
from app.schemas.schemas import ProjectResponse

router = APIRouter(tags=["Projects"])

@router.get("/projects", response_model=List[ProjectResponse])
def get_projects(category: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Project).filter(Project.is_published == True)
    if category and category != "all":
        query = query.filter(Project.category == category)
    return query.order_by(Project.order_index, Project.created_at.desc()).all()

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id, Project.is_published == True).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
