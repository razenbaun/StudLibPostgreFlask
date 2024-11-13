from flask import Flask
from model.model import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://my_user:446977@localhost/lib'
    app.secret_key = 'secret_key_here'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from routes.index_routes import index_bp
    app.register_blueprint(index_bp)
    from routes.publishing_houses_routes import publishing_houses_bp
    app.register_blueprint(publishing_houses_bp)
    from routes.authors_routes import authors_bp
    app.register_blueprint(authors_bp)
    from routes.clients_routes import clients_bp
    app.register_blueprint(clients_bp)
    from routes.genre_routes import genre_bp
    app.register_blueprint(genre_bp)
    from routes.books_routes import books_bp
    app.register_blueprint(books_bp)
    from routes.agreement_routes import agreement_bp
    app.register_blueprint(agreement_bp)
    from routes.reservation_routes import reservation_bp
    app.register_blueprint(reservation_bp)
    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
