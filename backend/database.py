from datetime import datetime

import sqlalchemy as _sql
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm as _orm
from os import environ
from dotenv import load_dotenv

load_dotenv()

db_user = environ.get('POSTGRES_USER')
db_password = environ.get('POSTGRES_PASSWORD')
db_host = environ.get('DB_HOST')
db_name = environ.get('POSTGRES_DB')

tbl_name = 'notes'

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"

engine = _sql.create_engine(DATABASE_URL)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Note(Base):
    __tablename__ = tbl_name
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.Text, index=True)
    description = _sql.Column(_sql.Text, index=True)
    priority = _sql.Column(_sql.Text, index=True)
    date_created = _sql.Column(_sql.DateTime, default=datetime.utcnow)


table_exists = _sql.inspect(engine).has_table(tbl_name)

if not table_exists:
    Base.metadata.create_all(bind=engine)
