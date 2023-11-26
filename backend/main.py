from typing import TYPE_CHECKING, List

from fastapi import FastAPI, Depends, HTTPException

import sqlalchemy.orm as _orm

import schemas as _schemas
import services as _services
# from database import Base, tbl_name, engine

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = FastAPI()


@app.get("/api/notes", response_model=List[_schemas.Note])
async def get_notes(db: _orm.Session = Depends(_services.get_db)):
    return await _services.get_notes(db=db)


@app.get("/api/note/{note_id}/", response_model=_schemas.Note)
async def get_note(
        note_id: int,
        db: _orm.Session = Depends(_services.get_db)
):
    note = await _services.get_note(note_id=note_id, db=db)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} does not exist")
    return note


@app.post("/api/note", response_model=_schemas.Note)
async def create_note(
        note: _schemas.CreateNote,
        db: _orm.Session = Depends(_services.get_db)
):
    return await _services.create_note(note=note, db=db)


@app.delete("/api/note/{note_id}")
async def delete_note(
        note_id: int,
        db: _orm.Session = Depends(_services.get_db)
):
    note = await _services.get_note(note_id=note_id, db=db)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} does not exist")

    await _services.delete_note(note, db=db)
    return "Successfully deleted the note"


@app.put("/api/note/{note_id}/", response_model=_schemas.Note)
async def update_note(
        note_id: int,
        note_data: _schemas.CreateNote,
        db: _orm.Session = Depends(_services.get_db)
):
    note = await _services.get_note(note_id=note_id, db=db)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} does not exist")

    return await _services.update_note(note_data=note_data, note=note, db=db)
