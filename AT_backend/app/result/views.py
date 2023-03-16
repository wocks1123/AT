from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db import get_db

from .schemas import (
    ResultResponse
)
from .service import (
    get,
    get_all
)


result_router = APIRouter()


@result_router.get("/", response_model=List[ResultResponse])
def read_results(db_session: Session = Depends(get_db)):
    results = get_all(db_session=db_session)
    return results


@result_router.get("/{id}/video")
def get_video(id: int, db_session: Session = Depends(get_db)):
    result = get(db_session=db_session, id=id)
    if not result:
        return None
    return FileResponse(result.video_path)
