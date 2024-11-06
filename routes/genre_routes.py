from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.model import Genre, db

genre_bp = Blueprint('genre', __name__)


@genre_bp.route('/genres', methods=['GET'])
def get_genres():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)

    query = Genre.query

    if search_query:
        query = query.filter(Genre.genre.ilike(f"%{search_query}%"))

    per_page = 5
    pagination = query.paginate(page=page, per_page=per_page)

    return render_template('genres.html',
                           pagination=pagination,
                           search_query=search_query)


@genre_bp.route('/genres/add', methods=['GET', 'POST'])
def add_genre():
    if request.method == 'POST':
        genre_name = request.form['genre']
        new_genre = Genre(genre=genre_name)
        db.session.add(new_genre)
        db.session.commit()
        flash('Жанр успешно добавлен!', 'success')
        return redirect(url_for('genre.get_genres'))

    return render_template('add_genre.html')


@genre_bp.route('/genres/edit/<int:genre_id>', methods=['GET', 'POST'])
def edit_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)

    if request.method == 'POST':
        genre.genre = request.form['genre']
        db.session.commit()
        flash('Жанр успешно изменен!', 'success')
        return redirect(url_for('genre.get_genres'))

    return render_template('edit_genre.html', genre=genre)


@genre_bp.route('/genres/delete/<int:genre_id>', methods=['POST'])
def delete_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    db.session.delete(genre)
    db.session.commit()
    flash('Жанр успешно удален!', 'success')
    return redirect(url_for('genre.get_genres'))
