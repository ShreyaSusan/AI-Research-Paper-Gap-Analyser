from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4

from database import SessionLocal

from models import (
    ResearchProject,
    ResearchGap
)

from schemas import (
    GapCreate,
    GapStatusUpdate,
    GapResponse
)

from utils.helpers import (
    get_object_or_404,
    raise_server_error
)

router = APIRouter(
    prefix="",
    tags=["Research Gaps"]
)


# DATABASE DEPENDENCY
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# CREATE RESEARCH GAP
@router.post(
    "/gaps",
    response_model=GapResponse
)
def create_gap(
    gap: GapCreate,
    db: Session = Depends(get_db)
):

    try:

        # CHECK PROJECT EXISTS
        project = db.query(
            ResearchProject
        ).filter(
            ResearchProject.project_id == gap.project_id
        ).first()

        get_object_or_404(
            project,
            "Project"
        )

        # CREATE GAP
        new_gap = ResearchGap(
            gap_id=str(uuid4()),
            project_id=gap.project_id,
            gap_title=gap.gap_title,
            gap_description=gap.gap_description,
            research_opportunity=gap.research_opportunity,
            severity=gap.severity
        )

        db.add(new_gap)

        db.commit()

        db.refresh(new_gap)

        return new_gap

    except SQLAlchemyError:

        db.rollback()

        raise_server_error()


# GET ALL GAPS OF PROJECT
@router.get(
    "/projects/{project_id}/gaps",
    response_model=list[GapResponse]
)
def get_project_gaps(
    project_id: str,
    db: Session = Depends(get_db)
):

    gaps = db.query(
        ResearchGap
    ).filter(
        ResearchGap.project_id == project_id
    ).all()

    return gaps


# GET SINGLE GAP
@router.get(
    "/gaps/{gap_id}",
    response_model=GapResponse
)
def get_gap(
    gap_id: str,
    db: Session = Depends(get_db)
):

    gap = db.query(
        ResearchGap
    ).filter(
        ResearchGap.gap_id == gap_id
    ).first()

    gap = get_object_or_404(
        gap,
        "Research gap"
    )

    return gap


# UPDATE GAP STATUS
@router.patch(
    "/gaps/{gap_id}/status",
    response_model=GapResponse
)
def update_gap_status(
    gap_id: str,
    status_update: GapStatusUpdate,
    db: Session = Depends(get_db)
):

    try:

        gap = db.query(
            ResearchGap
        ).filter(
            ResearchGap.gap_id == gap_id
        ).first()

        gap = get_object_or_404(
            gap,
            "Research gap"
        )

        gap.status = status_update.status

        db.commit()

        db.refresh(gap)

        return gap

    except SQLAlchemyError:

        db.rollback()

        raise_server_error()


# DELETE GAP
@router.delete(
    "/gaps/{gap_id}"
)
def delete_gap(
    gap_id: str,
    db: Session = Depends(get_db)
):

    try:

        gap = db.query(
            ResearchGap
        ).filter(
            ResearchGap.gap_id == gap_id
        ).first()

        gap = get_object_or_404(
            gap,
            "Research gap"
        )

        db.delete(gap)

        db.commit()

        return {
            "message": "Gap deleted successfully"
        }

    except SQLAlchemyError:

        db.rollback()

        raise_server_error()