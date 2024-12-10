from flask import Blueprint, render_template, redirect, url_for, request, session, flash

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '1111':
            session['user'] = 'admin'
            flash('Logged in as admin')
            return redirect('/')
        elif username == 'user' and password == '1111':
            session['user'] = 'user'
            flash('Logged in as user')
            return redirect('/')
        else:
            flash('Invalid credentials')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully')
    return redirect(url_for('auth.login'))
