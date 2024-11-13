from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from model.model import db, PublishingHouse

publishing_houses_bp = Blueprint('publishing_houses', __name__)


@publishing_houses_bp.route('/publishing_houses', methods=['GET'])
def get_publishing_houses():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)

    query = PublishingHouse.query

    if search_query:
        query = query.filter(PublishingHouse.publishing_house_name.ilike(f"%{search_query}%"))

    per_page = 5
    pagination = query.paginate(page=page, per_page=per_page)

    return render_template('publishing_houses.html',
                           pagination=pagination,
                           search_query=search_query)


@publishing_houses_bp.route('/publishing_houses/new', methods=['GET'])
def new_publishing_house():
    return render_template('publishing_house.html')


@publishing_houses_bp.route('/publishing_houses', methods=['POST'])
def add_publishing_house():
    publishing_house_name = request.form.get('publishing_house_name')
    contact_information = request.form.get('contact_information')

    if not publishing_house_name:
        flash("Название Издательства не заполнено!")
        return redirect(url_for('publishing_houses.new_publishing_house'))

    new_house = PublishingHouse(
        publishing_house_name=publishing_house_name,
        contact_information=contact_information
    )
    db.session.add(new_house)
    db.session.commit()

    flash("Издательство добавлено!")
    return redirect(url_for('publishing_houses.get_publishing_houses'))


@publishing_houses_bp.route('/publishing_houses/delete/<int:house_id>', methods=['POST'])
def delete_publishing_house(house_id):
    if session.get('user') != 'admin':
        flash("У вас нет прав для удаления издательства!")
        return redirect(url_for('publishing_houses.get_publishing_houses'))

    house = PublishingHouse.query.get_or_404(house_id)
    db.session.delete(house)
    db.session.commit()
    flash("Издательство удалено успешно!")
    return redirect(url_for('publishing_houses.get_publishing_houses'))


@publishing_houses_bp.route('/publishing_houses/edit/<int:house_id>', methods=['GET'])
def edit_publishing_house(house_id):
    if session.get('user') != 'admin':
        flash("У вас нет прав для редактирования издательства!")
        return redirect(url_for('publishing_houses.get_publishing_houses'))

    house = PublishingHouse.query.get_or_404(house_id)
    return render_template('edit_publishing_house.html', house=house)


@publishing_houses_bp.route('/publishing_houses/update/<int:house_id>', methods=['POST'])
def update_publishing_house(house_id):
    house = PublishingHouse.query.get_or_404(house_id)
    house.publishing_house_name = request.form.get('publishing_house_name')
    house.contact_information = request.form.get('contact_information')

    db.session.commit()
    flash("Издательство обновлено успешно!")
    return redirect(url_for('publishing_houses.get_publishing_houses'))
