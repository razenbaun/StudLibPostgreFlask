from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.model import db, Reservation, Book, Client, Agreement
from datetime import datetime

reservation_bp = Blueprint('reservation', __name__)


@reservation_bp.route('/reservations', methods=['GET'])
def get_reservations():
    reservations = Reservation.query.all()
    return render_template('reservations.html', reservations=reservations)


@reservation_bp.route('/reservations/create', methods=['GET', 'POST'])
def create_reservation():
    if request.method == 'POST':
        book_id = request.form['book_id']
        client_id = request.form['client_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        book = Book.query.get(book_id)

        # Проверяем, достаточно ли книг в запасе для резервирования
        if book.quantity_in_stock <= 0:
            flash('Недостаточно книг в запасе для резервирования!', 'danger')
            return redirect(url_for('reservation.get_reservations'))

        # Создаем новое резервирование
        new_reservation = Reservation(
            start_date=start_date,
            end_date=end_date,
            book_id=book_id,
            client_id=client_id
        )

        # Уменьшаем количество книг в запасе
        book.quantity_in_stock -= 1

        db.session.add(new_reservation)
        db.session.commit()

        flash('Резервирование успешно создано!', 'success')
        return redirect(url_for('reservation.get_reservations'))

    books = Book.query.all()
    clients = Client.query.all()
    return render_template('create_reservation.html', books=books, clients=clients)


@reservation_bp.route('/reservations/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)

    if reservation:
        # Получаем книгу по book_id резервирования
        book = Book.query.get(reservation.book_id)

        # Увеличиваем количество книг в запасе
        book.quantity_in_stock += 1

        # Удаляем резервирование
        db.session.delete(reservation)
        db.session.commit()

        flash('Резервирование успешно отменено!', 'success')
    else:
        flash('Резервирование не найдено!', 'danger')

    return redirect(url_for('reservation.get_reservations'))


@reservation_bp.route('/reservations/close/<int:reservation_id>', methods=['POST'])
def close_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    new_agreement = Agreement(
        issuance_date=datetime.now().date(),
        book_id=reservation.book_id,
        client_id=reservation.client_id
    )

    db.session.add(new_agreement)

    db.session.delete(reservation)
    db.session.commit()

    flash('Резервирование успешно закрыто и соглашение создано!', 'success')
    return redirect(url_for('reservation.get_reservations'))
