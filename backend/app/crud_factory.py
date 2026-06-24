from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from .schemas import BaseModel
from .deps import get_db


def get_record_or_404(db: Session, model, record_id: int, detail: str):
    record = db.query(model).filter(model.id == record_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return record


def update_record(record, payload: dict):
    for field, value in payload.items():
        setattr(record, field, value)
    return record


def register_crud_routes(
    router: APIRouter,
    model,
    create_schema,
    update_schema,
    read_schema,
    resource_name: str,
):
    @router.post("/", response_model=read_schema, status_code=status.HTTP_201_CREATED)
    def create_item(payload: dict, db: Session = Depends(get_db)):
        validated_payload = create_schema(**payload)
        record = model(**validated_payload.dict())
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @router.get("/", response_model=List[read_schema])
    def list_items(db: Session = Depends(get_db)):
        return db.query(model).all()

    @router.get("/{item_id}", response_model=read_schema)
    def get_item(item_id: int, db: Session = Depends(get_db)):
        return get_record_or_404(db, model, item_id, f"{resource_name.title()} not found")

    @router.put("/{item_id}", response_model=read_schema)
    def update_item(item_id: int, payload: dict, db: Session = Depends(get_db)):
        record = get_record_or_404(db, model, item_id, f"{resource_name.title()} not found")
        validated_payload = update_schema(**payload)
        record = update_record(record, validated_payload.dict(exclude_unset=True))
        db.commit()
        db.refresh(record)
        return record

    @router.delete("/{item_id}")
    def delete_item(item_id: int, db: Session = Depends(get_db)):
        record = get_record_or_404(db, model, item_id, f"{resource_name.title()} not found")
        db.delete(record)
        db.commit()
        return {"message": f"{resource_name.title()} deleted successfully"}
