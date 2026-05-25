from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4

from database import SessionLocal
from models import ResearchProject
from schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse
)

from utils.helpers import (
    get_object_or_404,
    raise_server_error
)

router = APIRouter(
    prefix="/projects",
    tags=["Research Projects"]
)


# DATABASE DEPENDENCY
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# CREATE PROJECT
@router.post(
    "",
    response_model=ProjectResponse,
    summary="Create Research Project"
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):

    try:

        new_project = ResearchProject(
            project_id=str(uuid4()),
            project_title=project.project_title,
            description=project.description
        )

        db.add(new_project)

        db.commit()

        db.refresh(new_project)

        return new_project

    except SQLAlchemyError:

        db.rollback()

        raise_server_error()


# GET ALL PROJECTS
@router.get(
    "",
    response_model=list[ProjectResponse]
)
def get_projects(
    db: Session = Depends(get_db)
):

    projects = db.query(
        ResearchProject
    ).all()

    return projects


# GET SINGLE PROJECT
@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def get_project(
    project_id: str,
    db: Session = Depends(get_db)
):

    project = db.query(
        ResearchProject
    ).filter(
        ResearchProject.project_id == project_id
    ).first()

    project = get_object_or_404(
        project,
        "Project"
    )

    return project


# UPDATE PROJECT
@router.put(
    "/{project_id}",
    response_model=ProjectResponse
)
def update_project(
    project_id: str,
    updated_project: ProjectUpdate,
    db: Session = Depends(get_db)
):

    try:

        project = db.query(
            ResearchProject
        ).filter(
            ResearchProject.project_id == project_id
        ).first()

        project = get_object_or_404(
            project,
            "Project"
        )

        project.project_title = updated_project.project_title
        project.description = updated_project.description
        project.status = updated_project.status

        db.commit()

        db.refresh(project)

        return project

    except SQLAlchemyError:

        db.rollback()

        raise_server_error()


# DELETE PROJECT
@router.delete(
    "/{project_id}"
)
def delete_project(
    project_id: str,
    db: Session = Depends(get_db)
):

    try:

        project = db.query(
            ResearchProject
        ).filter(
            ResearchProject.project_id == project_id
        ).first()

        project = get_object_or_404(
            project,
            "Project"
        )

        db.delete(project)

        db.commit()

        return {
            "message": "Project deleted successfully"
        }

    except SQLAlchemyError:

        db.rollback()

        raise_server_error()