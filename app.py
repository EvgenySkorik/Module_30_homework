from flask_openapi3 import OpenAPI, Info
from database import db


def create_app():
    info = Info(title="homework_29_TugoseryAPI", version="1.0.0")
    app = OpenAPI(__name__, info=info, doc_prefix="/api/docs")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tugosery.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    with app.app_context():
        from models import Client, Parking, ClientParking

        db.create_all()

    from routes import clients_bp, parkings_bp, index_bp, cp_bp

    app.register_api(index_bp)
    app.register_api(clients_bp)
    app.register_api(parkings_bp)
    app.register_api(cp_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
