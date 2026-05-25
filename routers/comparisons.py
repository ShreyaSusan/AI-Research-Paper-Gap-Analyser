from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4

from database import SessionLocal

from models import (
    ResearchProject,
    ResearchPaper,
    PaperComparison
)

from schemas import (
    ComparisonCreate,
    ComparisonResponse
)

from utils.helpers import (
    get_object_or_404,
    raise_server_error
)

router = APIRouter(
    prefix="",
    tags=["Paper Comparisons"]
)

# DATABASE DEPENDENCY
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# CREATE PAPER COMPARISON
@router.post(
    "/comparisons",
    response_model=ComparisonResponse
)
def create_comparison(
    comparison: ComparisonCreate,
    db: Session = Depends(get_db)
):

    try:

        # CHECK PROJECT EXISTS
        project = db.query(
            ResearchProject
        ).filter(
            ResearchProject.project_id == comparison.project_id
        ).first()

        get_object_or_404(
            project,
            "Project"
        )

        # CHECK PAPER 1 EXISTS
        paper_1 = db.query(
            ResearchPaper
        ).filter(
            ResearchPaper.paper_id == comparison.paper_1_id
        ).first()

        get_object_or_404(
            paper_1,
            "Paper 1"
        )

        # CHECK PAPER 2 EXISTS
        paper_2 = db.query(
            ResearchPaper
        ).filter(
            ResearchPaper.paper_id == comparison.paper_2_id
        ).first()

        get_object_or_404(
            paper_2,
            "Paper 2"
        )

        # PREVENT SAME PAPER COMPARISON
        if comparison.paper_1_id == comparison.paper_2_id:

            raise HTTPException(
                status_code=400,
                detail="Cannot compare same paper"
            )

        # CREATE COMPARISON
        new_comparison = PaperComparison(
            comparison_id=str(uuid4()),
            project_id=comparison.project_id,
            paper_1_id=comparison.paper_1_id,
            paper_2_id=comparison.paper_2_id,
            similarities=comparison.similarities,
            differences=comparison.differences,
            methodology_comparison=comparison.methodology_comparison,
            limitations_comparison=comparison.limitations_comparison
        )

        db.add(new_comparison)

        db.commit()

        db.refresh(new_comparison)

        return new_comparison

    except SQLAlchemyError:

        db.rollback()

        raise_server_error()


# GET ALL COMPARISONS OF PROJECT
@router.get(
    "/projects/{project_id}/comparisons",
    response_model=list[ComparisonResponse]
)
def get_project_comparisons(
    project_id: str,
    db: Session = Depends(get_db)
):

    comparisons = db.query(
        PaperComparison
    ).filter(
        PaperComparison.project_id == project_id
    ).all()

    return comparisons


# GET SINGLE COMPARISON
@router.get(
    "/comparisons/{comparison_id}",
    response_model=ComparisonResponse
)
def get_comparison(
    comparison_id: str,
    db: Session = Depends(get_db)
):

    comparison = db.query(
        PaperComparison
    ).filter(
        PaperComparison.comparison_id == comparison_id
    ).first()

    comparison = get_object_or_404(
        comparison,
        "Comparison"
    )

    return comparison


# DELETE COMPARISON
@router.delete(
    "/comparisons/{comparison_id}"
)
def delete_comparison(
    comparison_id: str,
    db: Session = Depends(get_db)
):

    try:

        comparison = db.query(
            PaperComparison
        ).filter(
            PaperComparison.comparison_id == comparison_id
        ).first()

        comparison = get_object_or_404(
            comparison,
            "Comparison"
        )

        db.delete(comparison)

        db.commit()

        return {
            "message": "Comparison deleted successfully"
        }

    except SQLAlchemyError:

        db.rollback()

        raise_server_error()