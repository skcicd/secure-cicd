# This file defines the routes and views for the application.
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.models import register_user, verify_user


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

bp = Blueprint('main', __name__)
limiter = Limiter(key_func=get_remote_address)


# Home route
@bp.route('/')
def home():
    return render_template("index.html")

# Register page
@bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Limit to 5 requests per minute per IP
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password are required!", "error")
            return redirect(url_for('main.register'))

        if register_user(username, password):
            flash("User registered successfully!", "success")
            return redirect(url_for('main.home'))
        else:
            flash("User already exists!", "error")
            return redirect(url_for('main.register'))

    return render_template("register.html")

# Login page
@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Limit to 5 requests per minute per IP
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password are required!", "error")
            return redirect(url_for('main.login'))

        if verify_user(username, password):
            flash(f"Welcome, {username}!", "success")
            return redirect(url_for('main.home'))
        else:
            flash("Invalid credentials!", "error")
            return redirect(url_for('main.login'))

    return render_template("login.html")

