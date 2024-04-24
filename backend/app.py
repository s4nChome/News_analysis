from flask import Flask
from flask_cors import CORS 
from flask_sqlalchemy import SQLAlchemy
from config import Config


app = Flask(__name__)
CORS(app) 

app.config.from_object(Config)
db = SQLAlchemy(app)

# 导入api
from api import *

if __name__ == '__main__':
    app.run(debug=True)