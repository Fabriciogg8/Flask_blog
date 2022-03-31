from Blog_website import app, db

from Blog_website.forms import RegisterForm, LoginForm
from Blog_website.models import User, Blog, Comment

from flask import render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user
from flask import redirect, render_template, request, url_for, flash 


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    rform = RegisterForm()
    if rform.validate_on_submit():
        create_user = User(name = rform.username.data,
                           email = rform.email.data,
                           password = rform.password.data)
        db.session.add(create_user)
        db.session.commit()
        login_user(create_user)
        flash(f'Congrats! You are now logged in as {create_user.name.capitalize()}', category='success')

        return redirect(url_for('blog'))
    if rform.errors != {}: #If there are not errors from the validators
        for err_msg in rform.errors.values():
            flash(f'There was an error with creating a user {err_msg}', category='danger')
    return render_template("register.html", rform=rform)


@app.route("/login", methods=['GET', 'POST'])
def login():
    lform = LoginForm()
    if lform.validate_on_submit():
        attempted_user = User.query.filter_by(email=lform.email.data).first()
        if attempted_user and attempted_user.verify_password(attempted_password=lform.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.name}', category='success') 
            return redirect(url_for('blog'))
        else:
            flash('Invalid mail or incorrect password', category='danger')
    return render_template("login.html", lform=lform)


@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('home'))


@app.route("/blog")
def blog():
    return render_template("blog.html")