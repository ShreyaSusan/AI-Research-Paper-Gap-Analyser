from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4

from database import SessionLocal

from models import (
    ResearchGap,
    ResearchPaper,
    GapPaperMapping
)

from schemas import (
    GapPaperMappingCreate,
    GapPaperMappingResponse
)

from utils.helpers import (
    get_object_or_404,
    raise_server_error
)

router = APIRouter(
    prefix="",
    tags=["Gap Paper Mappings"]
)


# DATABASE DEPENDENCY
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# CREATE GAP PAPER MAPPING
@router.post(
    "/gap-paper-mappings",
    response_model=GapPaperMappingResponse
)
def create_gap_paper_mapping(
    mapping: GapPaperMappingCreate,
    db: Session = Depends(get_db)
):

    try:

        # CHECK GAP EXISTS
        gap = db.query(
            ResearchGap
        ).filter(
            ResearchGap.gap_id == mapping.gap_id
        ).first()

        get_object_or_404(
            gap,
            "Research gap"
        )

        # CHECK PAPER EXISTS
        paper = db.query(
            ResearchPaper
        ).filter(
            ResearchPaper.paper_id == mapping.paper_id
        ).first()

        get_object_or_404(
            paper,
            "Research paper"
        )

        # PREVENT DUPLICATE MAPPING
        existing_mapping = db.query(
            GapPaperMapping
        ).filter(
            GapPaperMapping.gap_id == mapping.gap_id,
            GapPaperMapping.paper_id == mapping.paper_id
        ).first()

        if existing_mapping:

            raise HTTPException(
                status_code=400,
                detail="Mapping already exists"
            )

        # CREATE MAPPING
        new_mapping = GapPaperMapping(
            mapping_id=str(uuid4()),
            gap_id=mapping.gap_id,
            paper_id=mapping.paper_id,
            relevance_reason=mapping.relevance_reason
        )

        db.add(new_mapping)

        db.commit()

        db.refresh(new_mapping)

        return new_mapping

    except SQLAlchemyError:

        db.rollback()

        raise_server_error()


# GET ALL PAPER MAPPINGS OF GAP
@router.get(
    "/gaps/{gap_id}/papers",
    response_model=list[GapPaperMappingResponse]
)
def get_gap_papers(
    gap_id: str,
    db: Session = Depends(get_db)
):

    mappings = db.query(
        GapPaperMapping
    ).filter(
        GapPaperMapping.gap_id == gap_id
    ).all()

    return mappings


# DELETE GAP PAPER MAPPING
@router.delete(
    "/gap-paper-mappings/{mapping_id}"
)
def delete_gap_paper_mapping(
    mapping_id: str,
    db: Session = Depends(get_db)
):

    try:

        mapping = db.query(
            GapPaperMapping
        ).filter(
            GapPaperMapping.mapping_id == mapping_id
        ).first()

        mapping = get_object_or_404(
            mapping,
            "Gap paper mapping"
        )

        db.delete(mapping)

        db.commit()

        return {
            "message": "Mapping deleted successfully"
        }

    except SQLAlchemyError:

        db.rollback()

        raise_server_error()