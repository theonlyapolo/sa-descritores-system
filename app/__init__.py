from flask import Flask, jsonify
from app.config import Config
from app.extensions import db, migrate, jwt, smorest_api, cors
from app.api.v1 import register_blueprints

def create_app(config_object=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)
    db.init_app(app); migrate.init_app(app, db); jwt.init_app(app); smorest_api.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    register_blueprints(smorest_api)
    @app.errorhandler(404)
    def not_found(error): return jsonify({"message":"Recurso não encontrado."}), 404
    return app
    return app
