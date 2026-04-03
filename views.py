from flask import Blueprint, render_template, request, redirect, url_for


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("homePage.html")

@views.route('/browse-page')
def browsePage():
    return render_template("browsePage.html")

@views.route('/contact-page')
def contactPage():
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

@views.route('/description-page')
def descriptionPage():
    # Dummy plant data for now
    plant = {
        'name': 'Snake Plant',
        'price': 25,
        'desc': 'The Snake Plant is a hardy, low-maintenance plant perfect for beginners. It thrives in low light conditions and requires minimal watering.',
        'image': 'homeBG.jpg'
    }
    return render_template("description.html", plant=plant)