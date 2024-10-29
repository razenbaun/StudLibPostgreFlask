from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.model import Agreement, Book, Client, db
from datetime import date

agreement_bp = Blueprint('agreement', __name__)


@agreement_bp.route('/agreements', methods=['GET'])
def get_agreements():
    agreements = Agreement.query.all()
    return render_template('agreements.html', agreements=agreements)


@agreement_bp.route('/agreements/create', methods=['GET', 'POST'])
def create_agreement():
    if request.method == 'POST':
        book_id = request.form['book_id']
        client_id = request.form['client_id']

        book = Book.query.get(book_id)
        if book.quantity_in_stock <= 0:
            flash('Книга недоступна для выдачи.', 'danger')
            return redirect(url_for('agreement.create_agreement'))

        new_agreement = Agreement(
            book_id=book_id,
            client_id=client_id,
            issuance_date=date.today()
        )
        db.session.add(new_agreement)

        book.quantity_in_stock -= 1

        db.session.commit()
        flash('Соглашение успешно создано!', 'success')
        return redirect(url_for('agreement.get_agreements'))

    books = Book.query.all()
    clients = Client.query.all()
    return render_template('create_agreement.html', books=books, clients=clients)


@agreement_bp.route('/agreements/close/<int:agreement_id>', methods=['POST'])
def close_agreement(agreement_id):
    agreement = Agreement.query.get_or_404(agreement_id)
    agreement.return_date = date.today()

    book = Book.query.get(agreement.book_id)
    book.quantity_in_stock += 1

    db.session.commit()
    flash('Соглашение успешно закрыто!', 'success')
    return redirect(url_for('agreement.get_agreements'))


@agreement_bp.route('/agreements/delete/<int:agreement_id>', methods=['POST'])
def delete_agreement(agreement_id):
    agreement = Agreement.query.get_or_404(agreement_id)
    db.session.delete(agreement)
    db.session.commit()
    flash('Соглашение успешно удалено!', 'success')
    return redirect(url_for('agreement.get_agreements'))
