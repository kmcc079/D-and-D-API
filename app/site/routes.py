from flask import Blueprint, render_template
from flask_login import login_required

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/account')
# @login_required
def account():
    return render_template('account.html')

@site.route('/about')
def about():
    return render_template('about.html')