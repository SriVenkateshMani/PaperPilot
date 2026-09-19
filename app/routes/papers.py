from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Paper
from app.schemas import PaperCreate

router = APIRouter(prefix="/papers", tags=["papers"])

@router.post("/")
def create_paper(
    data: PaperCreate,
    db: Session = Depends(get_db)
):
    paper = Paper(
        title = data.title,
        author = data.author
    )
    db.add(paper)
    db.commit()
    db.refresh(paper)

    return paper

@router.get("/")
def get_paper(db: Session = Depends(get_db)):
    return db.query(Paper).all()