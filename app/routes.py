# This file defines the routes and views for the application.
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash, current_app, session, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app import db, limiter
from app.models import User
import requests
from app.utils import login_required

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

bp = Blueprint('main', __name__)
#limiter = Limiter(key_func=get_remote_address)

# The code below lets the Flask server respond to browser requests for a favicon
@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(bp.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

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

        # Check if the user already exists
        if User.query.filter_by(username=username).first():
            flash("User already exists!", "error")
            return redirect(url_for('main.register'))

        # Create a new user
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("User registered successfully!", "success")
        return redirect(url_for('main.home'))
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

        # Check if the user exists
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id  # Store user ID in session
            session['username'] = user.username  # Optionally store the username
            flash(f"Welcome, {username}!", "success")
            return redirect(url_for('main.home'))
        else:
            flash("Invalid credentials!", "error")
            return redirect(url_for('main.login'))

    return render_template("login.html")

@bp.route('/logout')
@limiter.limit("5 per minute")  # Limit to 5 requests per minute per IP
def logout():
    session.clear()  # Clear the session
    flash("You have been logged out.", "info")
    return redirect(url_for('main.home'))

# Weather route
@bp.route('/weather', methods=['GET', 'POST'])
@login_required
@limiter.limit("5/minute")  # Limit to 5 requests per minute per IP
def weather():
    if request.method == 'POST':
        city = request.form.get('city')

        if not city:
            flash("Please enter a city name!", "error")
            return render_template('weather.html')

        # Fetch weather data
        api_key = current_app.config['OPENWEATHER_API_KEY']
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            city_name = weather_data['name']
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            return render_template('weather.html', city=city_name, temperature=temperature, description=description)
        else:
            flash("City not found or API error!", "error")

    return render_template('weather.html')