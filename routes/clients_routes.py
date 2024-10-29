from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.model import Client, db

clients_bp = Blueprint('clients', __name__)


@clients_bp.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)


@clients_bp.route('/clients/add', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        library_card_number = request.form['library_card_number']
        client_full_name = request.form['client_full_name']
        date_of_birth = request.form['date_of_birth']
        phone_number = request.form['phone_number']
        group = request.form['group']

        try:
            new_client = Client(
                library_card_number=library_card_number,
                client_full_name=client_full_name,
                date_of_birth=date_of_birth,
                phone_number=phone_number,
                group=group
            )
            db.session.add(new_client)
            db.session.commit()
            flash('Клиент успешно добавлен!', 'success')
        except Exception as e:
            db.session.rollback()  # Откат транзакции в случае ошибки
            flash('Ошибка при добавлении клиента: {}'.format(str(e)), 'danger')

        return redirect(url_for('clients.get_clients'))

    return render_template('add_client.html')


@clients_bp.route('/clients/edit/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method == 'POST':
        client.library_card_number = request.form['library_card_number']
        client.client_full_name = request.form['client_full_name']
        client.date_of_birth = request.form['date_of_birth']
        client.phone_number = request.form['phone_number']
        client.group = request.form['group']

        db.session.commit()
        flash('Клиент успешно изменён!', 'success')
        return redirect(url_for('clients.get_clients'))

    return render_template('edit_client.html', client=client)


@clients_bp.route('/clients/delete/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Клиент успешно удалён!', 'success')
    return redirect(url_for('clients.get_clients'))
