import datetime as _dt
import sqlalchemy as _sql

import database as _database


class Note(_database.Base):
    __tablename__ = _database.tbl_name
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.Text, index=True)
    description = _sql.Column(_sql.Text, index=True)
    priority = _sql.Column(_sql.Text, index=True)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
