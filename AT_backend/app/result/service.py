from typing import List, Optional, Dict

from app.db import CRUDBase
from .schemas import ResultCreate, ResultUpdate
from .models import Result


class ResultCRUD(CRUDBase[Result, ResultCreate, ResultUpdate]):
    ...


result_crud = ResultCRUD(Result)


def create(*, db_session, result_in: ResultCreate) -> Result:
    return result_crud.create(db_session=db_session, obj_in=result_in)


def create_by_dict(*, db_session, result_in: Dict) -> Result:
    return result_crud.create(db_session=db_session, obj_in=ResultCreate(**result_in))


def get(*, db_session, id: int) -> Result:
    return result_crud.get(db_session=db_session, id=id)


def get_all(*, db_session) -> List[Optional[Result]]:
    return result_crud.get_all(db_session=db_session)


def update(*, db_session, result: Result, result_in: ResultUpdate) -> Result:
    return result_crud.update(db_session=db_session, db_obj=result, obj_in=result_in)
