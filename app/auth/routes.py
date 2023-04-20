from forms import UserLoginForm, UserSignupForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignupForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            username = form.username.data
            email = form.email.data.lower()
            password = form.password.data
            print(email, password)

            new_user = User(username, email, password = password)

            db.session.add(new_user)
            db.session.commit()

            print(f'User {username} successfully added')
            return redirect(url_for('auth.login'))
    except:
        raise Exception('Invalid form data: User either already exists or form data is incorrect. Please check your form.', 'auth failed')
    return render_template('signup.html', form=form)


@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            user = User.query.filter(User.email == email).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                print('Login Successful!')
                return redirect(url_for('site.account'))
            else:
                flash(f'You have failed to in your attempt to access this content', 'auth-failed')
                print('Login Failed')
                return redirect(url_for('auth.login'))
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))