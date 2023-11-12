from flask import Flask

app = Flask(__name__)

from API.api import *

if __name__ == "__main__":
    app.run()
