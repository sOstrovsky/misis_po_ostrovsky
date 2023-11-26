import datetime as _dt
import pydantic as _pydantic


class _BaseNote(_pydantic.BaseModel):
    title: str
    description: str
    priority: int


class Note(_BaseNote):
    id: int
    date_created: _dt.datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class CreateNote(_BaseNote):
    pass
