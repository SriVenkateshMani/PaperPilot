from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routes.papers import router as papers_router
from app.routes.rag import router as rag_router

app = FastAPI()
Base.metadata.create_all(bind = engine)

app.include_router(papers_router)
app.include_router(rag_router)

@app.get("/ping")
def ping():
    return {"status": "ok"}