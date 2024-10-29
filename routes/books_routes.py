from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.model import Book, PublishingHouse, Author, db, Genre

books_bp = Blueprint('books', __name__)


@books_bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return render_template('books.html', books=books)


@books_bp.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_name = request.form['book_name']
        publishing_house_id = request.form['publishing_house_id']
        author_id = request.form['author_id']
        number_of_pages = request.form['number_of_pages']
        year_of_publishing = request.form['year_of_publishing']
        genre_id = request.form['genre_id']
        total_quantity = request.form['total_quantity']
        quantity_in_stock = request.form['quantity_in_stock']

        new_book = Book(
            book_name=book_name,
            publishing_house_id=publishing_house_id,
            author_id=author_id,
            number_of_pages=number_of_pages,
            year_of_publishing=year_of_publishing,
            genre_id=genre_id,
            total_quantity=total_quantity,
            quantity_in_stock=quantity_in_stock
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Книга успешно добавлена!', 'success')
        return redirect(url_for('books.get_books'))

    publishing_houses = PublishingHouse.query.all()
    authors = Author.query.all()
    genres = Genre.query.all()  # Добавлено
    return render_template('add_book.html', publishing_houses=publishing_houses, authors=authors, genres=genres)


@books_bp.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        book.book_name = request.form['book_name']
        book.publishing_house_id = request.form['publishing_house_id']
        book.author_id = request.form['author_id']
        book.number_of_pages = request.form['number_of_pages']
        book.year_of_publishing = request.form['year_of_publishing']
        book.genre_id = request.form['genre_id']
        book.total_quantity = request.form['total_quantity']
        book.quantity_in_stock = request.form['quantity_in_stock']

        db.session.commit()
        flash('Книга успешно изменена!', 'success')
        return redirect(url_for('books.get_books'))

    publishing_houses = PublishingHouse.query.all()
    authors = Author.query.all()
    genres = Genre.query.all()  # Добавлено
    return render_template('edit_book.html', book=book, publishing_houses=publishing_houses, authors=authors,
                           genres=genres)


@books_bp.route('/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Книга успешно удалена!', 'success')
    return redirect(url_for('books.get_books'))
