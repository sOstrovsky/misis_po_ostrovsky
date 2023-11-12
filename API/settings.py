import os
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path=dotenv_path, override=True)

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
SSLMODE = os.getenv("SSLMODE")
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
TARGET_SESSION_ATTRS = os.getenv("TARGET_SESSION_ATTRS")
