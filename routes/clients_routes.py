from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from model.model import Client, db

clients_bp = Blueprint('clients', __name__)


@clients_bp.route('/clients', methods=['GET'])
def get_clients():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)

    query = Client.query
    if search_query:
        query = query.filter(
            (Client.client_full_name.ilike(f"%{search_query}%")) |
            (Client.library_card_number.ilike(f"%{search_query}%"))
        )

    per_page = 5
    pagination = query.paginate(page=page, per_page=per_page)

    return render_template('clients.html', pagination=pagination, search_query=search_query)


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
            db.session.rollback()
            flash(f'Ошибка при добавлении клиента: {str(e)}', 'danger')

        return redirect(url_for('clients.get_clients'))

    return render_template('add_client.html')


@clients_bp.route('/clients/edit/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    if session.get('user') != 'admin':
        flash("У вас нет прав для изменения клиентов!", "danger")
        return redirect(url_for('clients.get_clients'))

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
    if session.get('user') != 'admin':
        flash("У вас нет прав для удаления клиентов!", "danger")
        return redirect(url_for('clients.get_clients'))

    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Клиент успешно удалён!', 'success')
    return redirect(url_for('clients.get_clients'))
