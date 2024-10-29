from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(255), nullable=False)
    publishing_house_id = db.Column(db.Integer, db.ForeignKey('publishing_houses.publishing_house_id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
    number_of_pages = db.Column(db.Integer)
    year_of_publishing = db.Column(db.Integer)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))
    total_quantity = db.Column(db.Integer)
    quantity_in_stock = db.Column(db.Integer)


class PublishingHouse(db.Model):
    __tablename__ = 'publishing_houses'

    publishing_house_id = db.Column(db.Integer, primary_key=True)
    publishing_house_name = db.Column(db.String(255), nullable=False)
    contact_information = db.Column(db.String(255))
    books = db.relationship('Book', backref='publishing_house', lazy=True)


class Author(db.Model):
    __tablename__ = 'authors'

    author_id = db.Column(db.Integer, primary_key=True)
    author_full_name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date)
    books = db.relationship('Book', backref='author', lazy=True)


class Client(db.Model):
    __tablename__ = 'clients'

    client_id = db.Column(db.Integer, primary_key=True)
    library_card_number = db.Column(db.String(50), nullable=False, unique=True)
    client_full_name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date)
    phone_number = db.Column(db.String(20))
    group = db.Column(db.String(50))


class Agreement(db.Model):
    __tablename__ = 'agreement'

    agreement_id = db.Column(db.Integer, primary_key=True)
    issuance_date = db.Column(db.Date, nullable=False, default=db.func.current_date())
    return_date = db.Column(db.Date)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)

    book = db.relationship('Book', backref='agreements', lazy=True)
    client = db.relationship('Client', backref='agreements', lazy=True)


class Reservation(db.Model):
    __tablename__ = 'reservation'

    reservation_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'))

    book = db.relationship('Book', backref='reservations')
    client = db.relationship('Client', backref='reservations')


class Genre(db.Model):
    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(100))
    books = db.relationship('Book', backref='genre', lazy=True)
