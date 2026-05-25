from sqlalchemy import Column, String, Text, DateTime, ForeignKey 
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base

class ResearchProject(Base):

    __tablename__ = "research_projects"

    project_id = Column(
        String,
        primary_key=True,
        index=True
    )

    project_title = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="active"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # RELATIONSHIP
    papers = relationship(
        "ResearchPaper",
        back_populates="project",
        cascade="all, delete"
    )
    gaps = relationship(
    "ResearchGap",
    cascade="all, delete"
    )
    comparisons = relationship(
    "PaperComparison",
    cascade="all, delete"
    )

class ResearchPaper(Base):

    __tablename__ = "research_papers"

    paper_id = Column(
        String,
        primary_key=True,
        index=True
    )

    project_id = Column(
        String,
        ForeignKey("research_projects.project_id")
    )

    batch_id = Column(String)

    title = Column(String)

    authors = Column(String)

    extracted_text = Column(Text)

    summary_text = Column(Text)

    upload_date = Column(DateTime)

    processing_status = Column(String)

    # RELATIONSHIP
    project = relationship(
        "ResearchProject",
        back_populates="papers"
    )
    comparisons_as_paper_1 = relationship(
    "PaperComparison",
    foreign_keys="PaperComparison.paper_1_id"
)

comparisons_as_paper_2 = relationship(
    "PaperComparison",
    foreign_keys="PaperComparison.paper_2_id"
)
gap_mappings = relationship(
    "GapPaperMapping",
    cascade="all, delete"
)
class PaperComparison(Base):

    __tablename__ = "paper_comparisons"

    comparison_id = Column(
        String,
        primary_key=True,
        index=True
    )

    project_id = Column(
        String,
        ForeignKey("research_projects.project_id")
    )

    paper_1_id = Column(
        String,
        ForeignKey("research_papers.paper_id")
    )

    paper_2_id = Column(
        String,
        ForeignKey("research_papers.paper_id")
    )

    similarities = Column(Text)

    differences = Column(Text)

    methodology_comparison = Column(Text)

    limitations_comparison = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
class ResearchGap(Base):

    __tablename__ = "research_gaps"

    gap_id = Column(
        String,
        primary_key=True,
        index=True
    )

    project_id = Column(
        String,
        ForeignKey("research_projects.project_id")
    )
    paper_mappings = relationship(
    "GapPaperMapping",
    cascade="all, delete"
)

    gap_title = Column(String)

    gap_description = Column(Text)

    research_opportunity = Column(Text)

    severity = Column(String)

    status = Column(
        String,
        default="identified"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
class GapPaperMapping(Base):

    __tablename__ = "gap_paper_mappings"

    mapping_id = Column(
        String,
        primary_key=True,
        index=True
    )

    gap_id = Column(
        String,
        ForeignKey("research_gaps.gap_id")
    )

    paper_id = Column(
        String,
        ForeignKey("research_papers.paper_id")
    )

    relevance_reason = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )