from fastapi import FastAPI

from database import engine
from models import Base

from routers.projects import router as project_router
from routers.papers import router as paper_router
from routers.comparisons import router as comparison_router
from routers.gaps import router as gap_router
from routers.mappings import router as mapping_router

app = FastAPI()

Base.metadata.create_all(bind=engine)


# INCLUDE ROUTERS
app.include_router(project_router)
app.include_router(paper_router)
app.include_router(comparison_router)
app.include_router(gap_router)
app.include_router(mapping_router)

# HOME ROUTE
@app.get("/")
def home():

    return {
        "message": "FastAPI working"
    }