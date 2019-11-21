import sys
import os
import flask_rest_api
import flask_sqlalchemy
import flask_migrate

from flask import Flask, make_response, redirect, send_from_directory, jsonify, request, current_app, render_template, json


## Initialize these objects here
# so they are accessible by `from app import db`
db = flask_sqlalchemy.SQLAlchemy(
    engine_options={"json_serializer": json.dumps} # use flask json to help serialize
)
migrate = flask_migrate.Migrate()

## Init and Config
def create_app():
    app = Flask(__name__, static_folder="build")

    if os.environ.get('FLASK_ENV') == 'development':
        app.config.from_object('app.config.DevelopmentConfig')
    else:
        app.config.from_object('app.config.ProductionConfig')
    
    ## Database
    db.init_app(app)
    migrate.init_app(app, db)
    
    ## Import models so flask-migrate can see
    from app.models import WorkflowExecution, TaskExecution, WeblogEvent, EcsEvent

    # Serve static files in production
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists("/app/build/" + path):
            return send_from_directory('build', path)
        else:
            return send_from_directory('build', 'index.html')

    
    ## API setup
    apis = flask_rest_api.Api(app)
    
    from app.api import api, external, admin, user
    apis.register_blueprint(api.WorkflowApi, url_prefix=app.config["API_PREFIX"])
    apis.register_blueprint(admin.AdminApi, url_prefix=app.config["API_PREFIX"])
    apis.register_blueprint(user.UserApi, url_prefix=app.config["API_PREFIX"])
    # Note: this route is NOT TO BE PROTECTED at the ALB level as it enforces an API_KEY for each route
    apis.register_blueprint(external.ExternalApi, url_prefix=app.config["EXTERNAL_API_PREFIX"])

    return app
