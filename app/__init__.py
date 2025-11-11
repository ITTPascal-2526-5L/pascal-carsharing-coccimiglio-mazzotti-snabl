from flask import Flask
from flask_cors import CORS
from .config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS configuration for local development
    # Allow the Nuxt.js frontend (localhost:3000) and common local origins.
    # In production, restrict origins to the real frontend domain.
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:3000",
                    "http://127.0.0.1:3000",
                    "http://localhost:5173",
                    "http://127.0.0.1:5173",
                    "*",
                ]
            }
        },
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "Accept", "Origin"],
    )

    # As an extra safeguard, ensure all responses include minimal CORS headers
    # This helps when some intermediary returns (e.g. 404/500) without CORS.
    @app.after_request
    def _add_cors_headers(response):
        response.headers.setdefault("Access-Control-Allow-Origin", "*")
        response.headers.setdefault(
            "Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS"
        )
        response.headers.setdefault(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,Accept,Origin"
        )
        return response

    from .routes import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app