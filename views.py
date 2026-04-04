from flask import Blueprint, render_template, request, redirect, url_for
from sql import execute_query

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("homePage.html")

@views.route('/browse-page')
def browsePage():
    plants = []
    
    try:
        from sql import execute_query
        # Fetch plants from database
        query = "SELECT * FROM plants LIMIT 12"
        plants = execute_query(query, fetch="all")
    except Exception as e:
        print(f"Database error: {e}")
        plants = []
    
    # If no plants in database, use dummy data
    if not plants:
        plants = [
            {'id': i, 'name': 'Snake Plant', 'price': 25.00, 'image': 'homeBG.jpg'}
            for i in range(1, 7)
        ]
    
    return render_template("browsePage.html", plants=plants)

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

@views.route('/description-page/<int:plant_id>')
def descriptionPage(plant_id):
    plant = None
    
    try:
        from sql import execute_query
        # Fetch plant from database
        query = "SELECT * FROM plants WHERE id = %s"
        plant = execute_query(query, (plant_id,), fetch="one")
    except Exception as e:
        print(f"Database error: {e}")
        plant = None
    
    # If plant not found, use dummy data
    if not plant:
        plant = {
            'id': plant_id,
            'name': 'Snake Plant',
            'price': 25.00,
            'desc': 'The Snake Plant is a hardy, low-maintenance plant perfect for beginners. It thrives in low light conditions and requires minimal watering. Known for its air-purifying qualities, this plant is ideal for bedrooms and offices.',
            'image': 'homeBG.jpg',
            'light': 'Low to Bright Indirect',
            'water': 'Every 2-3 weeks',
            'size': 'Medium',
            'pet_friendly': False
        }
    
    return render_template("description.html", plant=plant)