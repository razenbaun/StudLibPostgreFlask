from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.model import db, Author

authors_bp = Blueprint('authors', __name__)


@authors_bp.route('/authors', methods=['GET'])
def get_authors():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)

    query = Author.query

    if search_query:
        query = query.filter(Author.author_full_name.ilike(f"%{search_query}%"))

    per_page = 5
    pagination = query.paginate(page=page, per_page=per_page)

    return render_template('authors.html',
                           pagination=pagination,
                           search_query=search_query)


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
