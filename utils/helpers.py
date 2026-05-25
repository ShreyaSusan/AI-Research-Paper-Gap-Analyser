from fastapi import HTTPException
from sqlalchemy.orm import Session


# =========================
# COMMON NOT FOUND CHECK
# =========================

def get_object_or_404(
    db_object,
    object_name: str
):

    if not db_object:
        raise HTTPException(
            status_code=404,
            detail=f"{object_name} not found"
        )

    return db_object


# =========================
# COMMON SERVER ERROR
# =========================

def raise_server_error():

    raise HTTPException(
        status_code=500,
        detail="Internal server error"
    )