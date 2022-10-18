import hashlib
import re
import time

from argon2 import PasswordHasher
from flask import Blueprint, render_template, redirect, url_for, request, flash, session

from core.main import DB_LINK, DB_CONN, NAME, LOGGER, CONFIG
from core.tools import generateCode
from core.strings import ERROR, INFO

auth = Blueprint('auth', NAME)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    input_login = request.form.get('login')
    input_password = request.form.get('pass')
    remember = True if request.form.get('remember') else False

    sql_user_check = "SELECT * FROM accounts WHERE userName=%s OR email=%s LIMIT 1"
    DB_LINK.execute(sql_user_check, [input_login, input_login])
    data = DB_LINK.fetchone()
    if data is None:
        LOGGER.Info(ERROR['Login-1'], input_login)
        flash(ERROR['Login-1'])
        return redirect(url_for('auth.login'))

    argon = PasswordHasher(time_cost=4, parallelism=1)
    if not argon.verify(data['password'], input_password):
        LOGGER.Info(ERROR['Login-2'], input_login)
        flash(ERROR['Login-2'])
        return redirect(url_for('auth.login'))

    session['loggedin'] = True
    session['id'] = data['accountDBID']
    session['name'] = data['userName']

    return redirect(url_for('main.profile'))

@auth.route('/register')
def register():
    return render_template('register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    input_email = request.form.get('email')
    input_name = request.form.get('name')
    input_password = request.form.get('pass')
    input_password2 = request.form.get('repass')

    if len(input_name) > 20 or len(input_name) < 3:
        LOGGER.Info(ERROR['Register-2'], input_name, input_email)
        flash(ERROR['Register-2'])
        return redirect(url_for('auth.register'))

    if len(input_password) < 8:
        LOGGER.Info(ERROR['Register-3'], input_name, input_email)
        flash(ERROR['Register-3'])
        return redirect(url_for('auth.register'))

    if input_password != input_password2:
        LOGGER.Info(ERROR['Register-4'], input_name, input_email)
        flash(ERROR['Register-4'])
        return redirect(url_for('auth.register'))

    if not re.match(r'[^@]+@[^@]+\.[^@]+', input_email):
        LOGGER.Info(ERROR['Register-5'], input_name, input_email)
        flash(ERROR['Register-5'])
        return redirect(url_for('auth.register'))

    if not re.match(r'[A-Za-z0-9]+', input_name):
        LOGGER.Info(ERROR['Register-6'], input_name, input_email)
        flash(ERROR['Register-6'])
        return redirect(url_for('auth.register'))

    if not input_email or not input_name or not input_password or not input_password2:
        LOGGER.Info(ERROR['Register-7'], input_name, input_email)
        flash(ERROR['Register-7'])
        return redirect(url_for('auth.register'))

    # Check if user exists
    sql_user_check = "SELECT * FROM accounts WHERE userName=%s OR email=%s LIMIT 1"
    DB_LINK.execute(sql_user_check, [input_name, input_email])
    data = DB_LINK.fetchone()
    if data is not None:
        LOGGER.Info(ERROR['Register-1'], input_name, input_email)
        flash(ERROR['Register-1'])
        return redirect(url_for('auth.register'))

    argon = PasswordHasher(time_cost=4, parallelism=1)
    password = argon.hash(input_password)
    ip_address = request.remote_addr
    authKey = hashlib.md5((generateCode(10)).encode()).hexdigest()
    register_time = int(time.time())

    # Check if mail needs to be confirmed
    if CONFIG['Configs']['confirm_acc'] == "yes":
        email_verify = hashlib.md5(generateCode(10).encode()).hexdigest()
    else:
        email_verify = "-1"

    sql_user_new = "INSERT INTO accounts SET userName=%s, password=%s, email=%s, emailVerify=%s, authKey=%s, ip=%s, registerTime=%s"
    DB_LINK.execute(sql_user_new, [input_name, password, input_email, email_verify, authKey, ip_address, register_time])
    DB_CONN.commit()

    LOGGER.Info(INFO['Register-5'].format(input_name), input_email)
    flash(INFO['Register-5'].format(input_name))
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    return redirect(url_for('main.index'))