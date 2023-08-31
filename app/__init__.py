# flask
from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)

    # Register blueprints here
    # local
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
