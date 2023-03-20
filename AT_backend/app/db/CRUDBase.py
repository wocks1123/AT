from typing import List, Type, TypeVar, Generic

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.BaseClass import Base


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(self, db_session: Session) -> List[ModelType]:
        return db_session.query(self.model).all()

    def get(self, db_session: Session, id: int) -> ModelType:
        item = db_session.query(self.model).filter(self.model.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    def create(self, db_session: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def update(
        self, db_session: Session, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def delete(self, db_session: Session, id: int) -> ModelType:
        obj = db_session.query(self.model).get(id)
        if obj:
            db_session.delete(obj)
            db_session.commit()
            return obj
        else:
            raise HTTPException(status_code=404, detail="Item not found")

    def delete_all(self, db_session: Session) -> int:
        count = db_session.query(self.model).delete()
        db_session.commit()
        return count
