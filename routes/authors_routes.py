from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.model import db, Author

authors_bp = Blueprint('authors', __name__)


# Отображение всех авторов
@authors_bp.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    return render_template('authors.html', authors=authors)


# Добавление нового автора
@authors_bp.route('/authors/add', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        author_full_name = request.form.get('author_full_name')
        date_of_birth = request.form.get('date_of_birth')

        new_author = Author(author_full_name=author_full_name, date_of_birth=date_of_birth)
        db.session.add(new_author)
        db.session.commit()
        flash('Автор успешно добавлен!', 'success')
        return redirect(url_for('authors.get_authors'))

    return render_template('add_author.html')


# Удаление автора
@authors_bp.route('/authors/delete/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    author = Author.query.get(author_id)
    if author:
        db.session.delete(author)
        db.session.commit()
        flash('Автор успешно удалён!', 'success')
    else:
        flash('Автор не найден!', 'error')
    return redirect(url_for('authors.get_authors'))


# Изменение данных автора
@authors_bp.route('/authors/edit/<int:author_id>', methods=['GET', 'POST'])
def edit_author(author_id):
    author = Author.query.get(author_id)
    if request.method == 'POST':
        author.author_full_name = request.form.get('author_full_name')
        author.date_of_birth = request.form.get('date_of_birth')

        db.session.commit()
        flash('Данные автора успешно обновлены!', 'success')
        return redirect(url_for('authors.get_authors'))

    return render_template('edit_author.html', author=author)
