from typing import TYPE_CHECKING, List

import database as _database
# import models as _models
import schemas as _schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_note(note: _schemas.CreateNote, db: "Session") -> _schemas.Note:
    note = _database.Note(**note.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return _schemas.Note.model_validate(note)


async def get_notes(db: "Session") -> List[_schemas.Note]:
    notes = db.query(_database.Note).all()
    return list(map(_schemas.Note.model_validate, notes))


async def get_note(note_id: int, db: "Session") -> List[_schemas.Note]:
    note = db.query(_database.Note).filter(_database.Note.id == note_id).first()
    return note


async def delete_note(note: _database.Note, db: "Session"):
    db.delete(note)
    db.commit()


async def update_note(note_data: _schemas.CreateNote, note: _database.Note, db: "Session") -> _schemas.Note:
    note.title = note_data.title
    note.description = note_data.description
    note.priority = note_data.priority

    db.commit()
    db.refresh(note)
    return _schemas.Note.model_validate(note)
