from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from flask.helpers import get_root_path
from dash import Dash
import dash_bootstrap_components as dbc

csrf = CSRFProtect()
csrf._exempt_views.add('dash.dash.dispatch')
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class_name):
    """
    Initialise the Flask application.
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class_name)

    csrf.init_app(app)
    db.init_app(app)
    register_dashapp(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    with app.app_context():
        db.create_all()

    from flask_app.main.routes import main_bp
    app.register_blueprint(main_bp)
    
    from flask_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app


def register_dashapp(app):
    from flask_app.dash_app.helper.layout import layout
    from flask_app.dash_app.helper.callbacks import register_callbacks

    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width,initial-scale=1, shrink-to-fit=no"
    }

    dashapp = Dash(
        __name__,
        server=app,
        url_base_pathname='/dashboard/',
        assets_folder=get_root_path(__name__) + '/dashboard/assets/',
        meta_tags=[meta_viewport],
        external_stylesheets=[dbc.themes.LUX]
    )

    with app.app_context():
        dashapp.title = 'Dashboard'
        dashapp.layout = layout
        register_callbacks(dashapp)

    _protect_dash_views(dashapp)


def _protect_dash_views(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.routes_pathname_prefix):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])
            