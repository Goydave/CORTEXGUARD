from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register your routes blueprint
    from .routes import main
    app.register_blueprint(main)

    return app

# Expose the app instance for flask CLI
app = create_app()
