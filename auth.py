from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from config import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        password = request.form.get('password')

        user = User.query.filter_by(first_name=first_name).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category='success')
                login_user(user)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category='error')
        
        else:
            flash("Email does not exist", category='error')
        
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        phone_num = request.form.get("phoneNum")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(first_name=first_name).first()

        if user:
            flash("Email already exists.", category='error')

        elif len(first_name) < 2:
            flash("First name must be greater than 1 character. ", category='error')
        
        elif len(last_name) < 2:
            flash("last name must be greater than 1 character. ", category='error')

        elif len(phone_num) < 2:
            flash("Phone number must be consist of numbers. ", category='error')

        elif password1 != password2:
            flash("Passwords don't match. ", category='error')

        elif len(password1) < 7:
            flash("Password must be at least 7 characters. ", category='error')

        else:
            new_user = User(first_name=first_name, last_name=last_name, phone=phone_num,
                            password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(user)
            flash("Account created !", category='success')
            return redirect(url_for('views.home'))  # I called home function in views.py

    return render_template("sign_up.html", user=current_user)