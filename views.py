from flask import Blueprint, render_template, request, redirect, url_for
from sql import execute_query

views = Blueprint('views', __name__)

@views.route('/')
def home():
    popular_plants = []
    
    try:
        # Fetch popular plants from database - you might want to add a 'popular' column or use some criteria
        query = "SELECT * FROM plants ORDER BY RAND() LIMIT 6"  # Random 6 plants as popular
        popular_plants = execute_query(query, fetch="all")
    except Exception as e:
        print(f"Database error: {e}")
        popular_plants = []
    
    # If no plants in database, use dummy data with actual plant images
    if not popular_plants:
        plant_images = [
            'Aloe_Plant.jpg', 'Calathea_Medallion.jpg', 'Fiddle_Plant.jpg',
            'Snake_Plant.jpg', 'Spider_Plant.jpg', 'plant1.jpg'
        ]
        plant_names = [
            'Aloe Plant', 'Calathea Medallion', 'Fiddle Plant',
            'Snake Plant', 'Spider Plant', 'Monstera'
        ]
        plant_prices = [19.99, 34.99, 29.99, 24.99, 22.99, 39.99]
        
        popular_plants = [
            {'id': i, 'name': plant_names[i-1], 'price': plant_prices[i-1], 'image': plant_images[i-1]}
            for i in range(1, 7)
        ]
    
    return render_template("homePage.html", popular_plants=popular_plants)

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
    user_id = 1  # TEMP until login system is done

    # 1. Load user info
    user = execute_query(
        "SELECT first_name, last_name, email FROM user_base WHERE user_id = %s",
        (user_id,),
        fetch="one"
    )

    # 2. Get cartID
    cart_row = execute_query(
        "SELECT cartID, isGift FROM Cart WHERE user_id = %s",
        (user_id,),
        fetch="one"
    )

    if not cart_row:
        return render_template("checkOutPage.html", cart_items=[], total=0, user=user, isGift=False)

    cart_id = cart_row["cartID"]
    isGift = cart_row["isGift"]

    # 3. Load cart items
    cart_items = execute_query("""
        SELECT 
            ci.cartItemID,
            p.plantID,
            p.commonName,
            p.price,
            p.imageUrl,
            ci.quantity,
            (p.price * ci.quantity) AS subtotal
        FROM Cart_Items ci
        JOIN Plants p ON ci.plantID = p.plantID
        WHERE ci.cartID = %s
    """, (cart_id,), fetch="all")

    # 4. Load total
    total_row = execute_query("""
        SELECT SUM(p.price * ci.quantity) AS total
        FROM Cart_Items ci
        JOIN Plants p ON ci.plantID = p.plantID
        WHERE ci.cartID = %s
    """, (cart_id,), fetch="one")

    total = total_row["total"] if total_row["total"] else 0

    # 5. Delivery + shipping placeholders
    delivery_method = "Standard Delivery (3–5 days)"
    shipping_method = "Home Delivery"

    return render_template("checkOutPage.html", cart_items=cart_items, total=total, user=user, isGift=isGift, delivery_method=delivery_method, shipping_method=shipping_method)

@views.route('/process-checkout', methods=['POST'])
def processCheckout():
    user_id = 1  # TEMP

    # 1. Get cartID
    cart_row = execute_query(
        "SELECT cartID FROM Cart WHERE user_id = %s",
        (user_id,),
        fetch="one"
    )

    if not cart_row:
        return redirect(url_for('views.purchaseConfirmPage'))

    cart_id = cart_row["cartID"]

    # 2. Calculate total
    total_row = execute_query("""
        SELECT SUM(p.price * ci.quantity) AS total
        FROM Cart_Items ci
        JOIN Plants p ON ci.plantID = p.plantID
        WHERE ci.cartID = %s
    """, (cart_id,), fetch="one")

    total = total_row["total"] if total_row["total"] else 0

    # 3. Create order
    order_id = execute_query("""
        INSERT INTO Orders (user_id, totalAmount, isGift, shippingAddressAtTime)
        VALUES (%s, %s, %s, %s)
    """, (user_id, total, False, "Default Address"), fetch="none")

    # 4. Insert order items
    execute_query("""
        INSERT INTO Order_Items (orderID, plantID, quantity, priceAtPurchase)
        SELECT 
            %s,
            ci.plantID,
            ci.quantity,
            p.price
        FROM Cart_Items ci
        JOIN Plants p ON ci.plantID = p.plantID
        WHERE ci.cartID = %s
    """, (order_id, cart_id), fetch="none")

    # 5. Clear cart
    execute_query("DELETE FROM Cart_Items WHERE cartID = %s", (cart_id,), fetch="none")

    return redirect(url_for('views.purchaseConfirmPage'))

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