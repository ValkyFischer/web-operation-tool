from flask import Blueprint, render_template, session, url_for, redirect
from core.main import NAME

public = Blueprint('main', NAME)

@public.route('/')
def index():
    return render_template('index.html')

@public.route('/profile')
def profile():
    if "loggedin" in session:
        return render_template('profile.html', name=session['name'])
    else:
        return redirect(url_for('auth.login'))