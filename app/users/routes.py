from flask import Blueprint, redirect, render_template, url_for, request, current_app

from app.users.services.edit_company import edit_company
from .models import User, Company
from app.users.services.create_user import create_user
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.users.services.create_user import create_user
from app.users.services.create_company import create_company
from app.users.services.user_settings import user_settings
from app.users.services.check_current_user import check_current_user
from app.users.models import User, Company

blueprint = Blueprint('users', __name__)

### root ### 
@blueprint.route('/<user_id>')
@login_required
def user(user_id):

    user = User.query.filter_by(id=user_id).first()

    if check_current_user(user):
        companies = Company.query.filter_by(user_id=user_id)
        return render_template('/users/user.html', user=user, companies=companies)
    else:
        return "Permission Denied: You are not authorized to view this content"

    


### signup ###
@blueprint.get('/signup')
def get_signup():
    return render_template("users/signup.html")

@blueprint.post('/signup')
def post_signup():
    try:
        if User.query.filter_by(user_email=request.form.get('email')).first():
            raise Exception ('Email already taken.')
        elif request.form.get('password') != request.form.get('password_confirmation'):
            raise Exception('Passwords do not match.')
        
        user = create_user(request.form)
        login_user(user)
        return redirect(url_for('users.user', user_id=user.id))
    
    except Exception as error_message:
        error = error_message or 'An error occurred while creating a user. Please make sure to enter valid data.'
        return render_template('users/signup.html', error=error)

@blueprint.route('/sign-up')
@blueprint.route('/anmeldung')
@blueprint.route('/registration')
def redirect_signup():
    return redirect(url_for('users.get_signup'))


### login ###
@blueprint.get('/login')
def get_login():
    return render_template("users/login.html")

@blueprint.post('/login')
def post_login():
    try:
        user = User.query.filter_by(user_email=request.form.get('email')).first()
        if not user:
            raise Exception('Email address not found.')
        elif not check_password_hash(user.password, request.form.get('password')):
            raise Exception('Incorrect Password.')
        
        login_user(user)
        return redirect(url_for('users.user', user_id=user.id))
    
    except Exception as error_message:
        error = error_message or 'An error occurred while logging in. Please verify your email and password.'
        return render_template('users/login.html', error=error)


### logout ###
@blueprint.get('/logout')
def get_logout():
    logout_user()
    return redirect(url_for('users.get_login'))

### add account ###
@blueprint.get('/<user_id>/create_company')
def get_create_company(user_id):

    user = User.query.filter_by(id=user_id).first()

    if check_current_user(user):
        company = create_company(user_id)
        company_id = company.id

        return redirect(url_for('users.get_company', user_id=user_id, company_id=company_id))
    else:
        return "Permission Denied: You are not authorized to view this content"


### edit account ###
@blueprint.get('/<user_id>/company/<company_id>')
def get_company(user_id, company_id):

    user = User.query.filter_by(id=user_id).first()

    if check_current_user(user):
        company = Company.query.filter_by(id=company_id).first()
        if company.user_id == current_user.id:
            return render_template('/users/company.html', user=user, company=company)
        else:
            return "Permission Denied: You are not authorized to view this content"
    else:
        return "Permission Denied: You are not authorized to view this content"

@blueprint.post('/<user_id>/company/<company_id>')
def post_company(user_id, company_id):

    company = Company.query.filter_by(id=company_id).first()
    try:
        if request.form.get('user_password_') != request.form.get('user_password_confirm'):
            raise Exception('Passwords do not match.')
        edit_company(request.form, company)
        return redirect(url_for('users.user', user_id=user_id))

    except Exception as error_message:
        error = error_message or 'An error occurred while changing your password. Please try again.'
        return render_template('users/get_company', error=error)

### settings ###
@blueprint.get('/<user_id>/settings')
def get_settings(user_id):

    user = User.query.filter_by(id=user_id).first()

    if check_current_user(user):
        user = User.query.filter_by(id=user_id).first()
        return render_template("users/settings.html", user=user)
    else:
        return "Permission Denied: You are not authorized to view this content"

@blueprint.post('/<user_id>/settings')
def post_user_settings(user_id):

    user = User.query.filter_by(id=user_id).first()
    user_settings(request.form, user)
    
    return redirect(url_for('users.user', user_id=user_id))

### delete user ###
@blueprint.get('/<user_id>/deleteuser')
def delete_user(user_id):

    user = User.query.filter_by(id=user_id).first()
    if check_current_user(user):
        current_user.delete()
        return redirect(url_for('users.get_login'))

    else:
        return "Permission Denied: You are not authorized to view this content"


### delete company ### 
@blueprint.get('/<user_id>/company/<company_id>/deletecompany')
def delete_company(user_id, company_id):

    user = User.query.filter_by(id=user_id).first()

    if check_current_user(user):
        company = Company.query.filter_by(id=company_id).first()
        if company.user_id == current_user.id:
            user_id = current_user.id
            company.delete()
        else:
            return "Permission Denied: You are not authorized to view this content"
    else:
        return "Permission Denied: You are not authorized to view this content"

    return redirect(url_for('users.user', user_id=user_id))