from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
codex/desenvolver-api-rest-para-gestao-pedagogica-f1yib9
smorest_api = Api()
cors = CORS()
