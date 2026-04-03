from flask import Blueprint, render_template, request, redirect, url_for
from sql import execute_query

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("homePage.html")

@views.route('/browse-page')
def browsePage():
    return render_template("browsePage.html")

@views.route('/contact-page', methods=['GET', 'POST'])
def contactPage():
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        user_message = request.form.get('user_message')
        query = "INSERT INTO Contact_Submissions(name, email, messageText) VALUES (%s, %s, %s)"
        params = (user_name, user_email, user_message)
        execute_query(query, params, fetch='none')
        return redirect(url_for('views.emailConfirmPage'))
    return render_template("contactPage.html")

@views.route('/check-out-page')
def checkOutPage():
    return render_template("checkOutPage.html")

@views.route('/detail-page')
def detailPage():
    return render_template("detailPage.html")

@views.route('/log-in-page')
def logInPage():
    return render_template("logInPage.html")

@views.route('/sign-up-page')
def signUpPage():
    return render_template("signUpPage.html")

@views.route('/favorites-page')
def favoritesPage():
    return render_template("favoritesPage.html")

@views.route('/cart-page')
def cartPage():
    return render_template("cartPage.html")

@views.route('/email-confirm-page')
def emailConfirmPage():
    return render_template("emailConfirmPage.html")

@views.route('/purchase-confirm-page')
def purchaseConfirmPage():
    return render_template("purchaseConfirmPage.html")