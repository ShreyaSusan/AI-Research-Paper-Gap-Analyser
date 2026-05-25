from pydantic import BaseModel, Field, field_validator
from datetime import datetime


# =========================
# COMMON VALIDATION FUNCTION
# =========================
def validate_not_empty(value: str, field_name: str):

    if not value or not value.strip():
        raise ValueError(f"{field_name} cannot be empty")

    return value.strip()


# =========================
# PROJECT SCHEMAS
# =========================

class ProjectCreate(BaseModel):

    project_title: str = Field(..., min_length=3, max_length=200)

    description: str = Field(..., min_length=10, max_length=1000)

    @field_validator("project_title")
    @classmethod
    def validate_project_title(cls, value):
        return validate_not_empty(value, "Project title")

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        return validate_not_empty(value, "Description")


class ProjectUpdate(BaseModel):

    project_title: str = Field(..., min_length=3, max_length=200)

    description: str = Field(..., min_length=10, max_length=1000)

    status: str

    @field_validator("project_title")
    @classmethod
    def validate_project_title(cls, value):
        return validate_not_empty(value, "Project title")

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        return validate_not_empty(value, "Description")

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):

        allowed_status = ["active", "completed", "archived"]

        value = value.strip().lower()

        if value not in allowed_status:
            raise ValueError(
                f"Status must be one of {allowed_status}"
            )

        return value


class ProjectResponse(BaseModel):

    project_id: str

    project_title: str

    description: str

    status: str

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True


# =========================
# PAPER SCHEMAS
# =========================

class PaperCreate(BaseModel):

    project_id: str

    batch_id: str = Field(..., min_length=2, max_length=100)

    title: str = Field(..., min_length=3, max_length=300)

    authors: str = Field(..., min_length=3, max_length=500)

    extracted_text: str = Field(..., min_length=20)

    summary_text: str = Field(..., min_length=10)

    processing_status: str

    @field_validator(
        "batch_id",
        "title",
        "authors",
        "extracted_text",
        "summary_text"
    )
    @classmethod
    def validate_text_fields(cls, value):
        return validate_not_empty(value, "Field")

    @field_validator("processing_status")
    @classmethod
    def validate_processing_status(cls, value):

        allowed_status = [
            "pending",
            "processing",
            "completed",
            "failed"
        ]

        value = value.strip().lower()

        if value not in allowed_status:
            raise ValueError(
                f"Processing status must be one of {allowed_status}"
            )

        return value


class PaperStatusUpdate(BaseModel):

    processing_status: str

    @field_validator("processing_status")
    @classmethod
    def validate_processing_status(cls, value):

        allowed_status = [
            "pending",
            "processing",
            "completed",
            "failed"
        ]

        value = value.strip().lower()

        if value not in allowed_status:
            raise ValueError(
                f"Processing status must be one of {allowed_status}"
            )

        return value


class PaperSummaryUpdate(BaseModel):

    summary_text: str = Field(..., min_length=10)

    @field_validator("summary_text")
    @classmethod
    def validate_summary(cls, value):
        return validate_not_empty(value, "Summary text")


class PaperResponse(BaseModel):

    paper_id: str

    project_id: str

    batch_id: str

    title: str

    authors: str

    extracted_text: str

    summary_text: str

    processing_status: str

    class Config:
        from_attributes = True
# =========================
# PAPER COMPARISON SCHEMAS
# =========================

class ComparisonCreate(BaseModel):

    project_id: str

    paper_1_id: str

    paper_2_id: str

    similarities: str = Field(..., min_length=10)

    differences: str = Field(..., min_length=10)

    methodology_comparison: str = Field(..., min_length=10)

    limitations_comparison: str = Field(..., min_length=10)

    @field_validator(
        "similarities",
        "differences",
        "methodology_comparison",
        "limitations_comparison"
    )
    @classmethod
    def validate_text_fields(cls, value):

        return validate_not_empty(
            value,
            "Comparison field"
        )


class ComparisonResponse(BaseModel):

    comparison_id: str

    project_id: str

    paper_1_id: str

    paper_2_id: str

    similarities: str

    differences: str

    methodology_comparison: str

    limitations_comparison: str

    created_at: datetime

    class Config:
        from_attributes = True
# =========================
# RESEARCH GAP SCHEMAS
# =========================

class GapCreate(BaseModel):

    project_id: str

    gap_title: str = Field(..., min_length=5)

    gap_description: str = Field(..., min_length=20)

    research_opportunity: str = Field(..., min_length=20)

    severity: str

    @field_validator(
        "gap_title",
        "gap_description",
        "research_opportunity"
    )
    @classmethod
    def validate_gap_fields(cls, value):

        return validate_not_empty(
            value,
            "Gap field"
        )

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, value):

        allowed = [
            "low",
            "medium",
            "high"
        ]

        value = value.strip().lower()

        if value not in allowed:
            raise ValueError(
                f"Severity must be one of {allowed}"
            )

        return value


class GapStatusUpdate(BaseModel):

    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):

        allowed = [
            "identified",
            "investigating",
            "resolved"
        ]

        value = value.strip().lower()

        if value not in allowed:
            raise ValueError(
                f"Status must be one of {allowed}"
            )

        return value


class GapResponse(BaseModel):

    gap_id: str

    project_id: str

    gap_title: str

    gap_description: str

    research_opportunity: str

    severity: str

    status: str

    created_at: datetime

    class Config:
        from_attributes = True
# =========================
# GAP PAPER MAPPING SCHEMAS
# =========================

class GapPaperMappingCreate(BaseModel):

    gap_id: str

    paper_id: str

    relevance_reason: str = Field(..., min_length=10)

    @field_validator("relevance_reason")
    @classmethod
    def validate_reason(cls, value):

        return validate_not_empty(
            value,
            "Relevance reason"
        )


class GapPaperMappingResponse(BaseModel):

    mapping_id: str

    gap_id: str

    paper_id: str

    relevance_reason: str

    created_at: datetime

    class Config:
        from_attributes = True