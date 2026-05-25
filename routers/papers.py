from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
from datetime import datetime

from database import SessionLocal

from models import (
    ResearchProject,
    ResearchPaper
)

from schemas import (
    PaperCreate,
    PaperStatusUpdate,
    PaperSummaryUpdate,
    PaperResponse
)

from utils.helpers import (
    get_object_or_404,
    raise_server_error
)

router = APIRouter(
    prefix="",
    tags=["Research Papers"]
)


# DATABASE DEPENDENCY
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# CREATE PAPER
@router.post(
    "/papers",
    response_model=PaperResponse
)
def create_paper(
    paper: PaperCreate,
    db: Session = Depends(get_db)
):

    try:

        # CHECK PROJECT EXISTS
        project = db.query(
            ResearchProject
        ).filter(
            ResearchProject.project_id == paper.project_id
        ).first()

        get_object_or_404(
            project,
            "Project"
        )

        # CREATE PAPER
        new_paper = ResearchPaper(
            paper_id=str(uuid4()),
            project_id=paper.project_id,
            batch_id=paper.batch_id,
            title=paper.title,
            authors=paper.authors,
            extracted_text=paper.extracted_text,
            summary_text=paper.summary_text,
            upload_date=datetime.utcnow(),
            processing_status=paper.processing_status
        )

        db.add(new_paper)

        db.commit()

        db.refresh(new_paper)

        return new_paper

    except SQLAlchemyError:

        db.rollback()

        raise_server_error()


# GET ALL PAPERS OF PROJECT
@router.get(
    "/projects/{project_id}/papers",
    response_model=list[PaperResponse]
)
def get_project_papers(
    project_id: str,
    db: Session = Depends(get_db)
):

    papers = db.query(
        ResearchPaper
    ).filter(
        ResearchPaper.project_id == project_id
    ).all()

    return papers


# GET SINGLE PAPER
@router.get(
    "/papers/{paper_id}",
    response_model=PaperResponse
)
def get_paper(
    paper_id: str,
    db: Session = Depends(get_db)
):

    paper = db.query(
        ResearchPaper
    ).filter(
        ResearchPaper.paper_id == paper_id
    ).first()

    paper = get_object_or_404(
        paper,
        "Paper"
    )

    return paper


# UPDATE PAPER STATUS
@router.patch(
    "/papers/{paper_id}/status",
    response_model=PaperResponse
)
def update_paper_status(
    paper_id: str,
    status_update: PaperStatusUpdate,
    db: Session = Depends(get_db)
):

    try:

        paper = db.query(
            ResearchPaper
        ).filter(
            ResearchPaper.paper_id == paper_id
        ).first()

        paper = get_object_or_404(
            paper,
            "Paper"
        )

        paper.processing_status = (
            status_update.processing_status
        )

        db.commit()

        db.refresh(paper)

        return paper

    except SQLAlchemyError:

        db.rollback()

        raise_server_error()


# UPDATE PAPER SUMMARY
@router.patch(
    "/papers/{paper_id}/summary",
    response_model=PaperResponse
)
def update_paper_summary(
    paper_id: str,
    summary_update: PaperSummaryUpdate,
    db: Session = Depends(get_db)
):

    try:

        paper = db.query(
            ResearchPaper
        ).filter(
            ResearchPaper.paper_id == paper_id
        ).first()

        paper = get_object_or_404(
            paper,
            "Paper"
        )

        paper.summary_text = (
            summary_update.summary_text
        )

        db.commit()

        db.refresh(paper)

        return paper

    except SQLAlchemyError:

        db.rollback()

        raise_server_error()


# DELETE PAPER
@router.delete(
    "/papers/{paper_id}"
)
def delete_paper(
    paper_id: str,
    db: Session = Depends(get_db)
):

    try:

        paper = db.query(
            ResearchPaper
        ).filter(
            ResearchPaper.paper_id == paper_id
        ).first()

        paper = get_object_or_404(
            paper,
            "Paper"
        )

        db.delete(paper)

        db.commit()

        return {
            "message": "Paper deleted successfully"
        }

    except SQLAlchemyError:

        db.rollback()

        raise_server_error()