from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
from pop import delete_accessory
import pop
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key for session management



def read_accessories_from_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

@app.route('/')
def index():
    return redirect(url_for('home'))
# Home page
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/base')
def base():
    return render_template('base.html')

# Login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'guest' and password == 'guest':
            session['user'] = 'guest'
            return render_template('user.html')
        elif username == 'admin' and password == 'admin123':
            session['user'] = 'admin'
            return render_template('admin.html')
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('home'))

    return render_template('login.html')
# User dashboard
@app.route('/user_dashboard')
def user_dashboard():
    if 'user' in session and session['user'] == 'guest':
        return render_template('user_dashboard.html')
    else:
        return redirect(url_for('login'))

# Admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' in session and session['user'] == 'admin':
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/view_stock')
def view_stock():
    if 'user' in session:
        accessories =read_accessories_from_file('pop.txt')
        print(accessories)  # Debugging: Print the accessories list
        return render_template('view_stock.html', accessories=accessories)
    return redirect(url_for('login'))

@app.route('/selled_items')
def selled_items():
    if 'user' in session and session['user'] == 'admin':
        return render_template('selled_items.html')
    return redirect(url_for('login'))
@app.route('/buy_selected', methods=['POST'])
def buy_selected():
    selected_items = request.form.getlist('selected_items')
    quantities = {}
    
    # Loop through selected items and their corresponding quantities
    for item_code in selected_items:
        quantity_key = f"quantity_{item_code}"
        quantity = int(request.form.get(quantity_key, 1))  # Default to 1 if not provided
        quantities[item_code] = quantity
    
    # Now you have the quantities for each selected item
    # Process the order, calculate total, etc.
    # Example: print the quantities
    for item_code, quantity in quantities.items():
        print(f"Item Code: {item_code}, Quantity: {quantity}")
    
    # Render the confirmation page or redirect as needed
    return render_template('buy_now.html', quantities=quantities)

@app.route('/view_report')
def view_report():
    if 'user' in session and session['user'] == 'admin':
        return render_template('view_report.html')
    return redirect(url_for('login'))

@app.route('/search')
def search():
    query = request.args.get('query', '')
    accessories = read_accessories_from_file('pop.txt')
    
    # Filter the accessories based on the search query
    filtered_accessories = [accessory for accessory in accessories if query.lower() in accessory['name'].lower()]
    
    if not filtered_accessories:
        flash("No items found", "error")
    
    return render_template('search_results.html', query=query, accessories=filtered_accessories)

    
    return render_template('search_results.html', query=query, results=results)
@app.route('/buy_now/<item_code>', methods=['GET', 'POST'])
def buy_now(item_code):
    accessories = read_accessories_from_file('pop.txt')
    item = next((accessory for accessory in accessories if accessory['code'] == item_code), None)
    
    if item is None:
        flash("Item not found", "error")
        return redirect(url_for('home'))

    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        # Process the order, calculate total, etc.
        return render_template('confirmation.html', item=item, quantity=quantity)
    
    # Ensure item is passed to the template here
    return render_template('buy_now.html', item=item)

@app.route('/add_items', methods=['GET', 'POST'])
def add_items():
    if 'user' in session and session['user'] == 'admin':
        if request.method == 'POST':
            name = request.form['name']
            code = request.form['code']
            description = request.form['description']
            remaining_items = int(request.form['remaining_items'])
            price_excl_vat = float(request.form['price_excl_vat'])
            pop.add_accessory(name, code, description, remaining_items, price_excl_vat)
            flash("Accessory added successfully!", "success")
            return redirect(url_for('view_stock'))
        return render_template('add_items.html')
    return redirect(url_for('login'))


@app.route('/delete_item', methods=['GET', 'POST'])
def delete_item():
    print("Rendering delete_item.html")
    if request.method == 'POST':
        code = request.form.get('code')
        print(f"Deleting accessory with code: {code}")
        delete_accessory(code)  # Call the delete function
        
        return redirect(url_for('delete_item'))
    return render_template('delete_item.html')


@app.route('/update_price/<code>', methods=['GET', 'POST'])
def update_price(code):
    if 'user' in session and session['user'] == 'admin':
        if request.method == 'POST':
            new_price = float(request.form['price_excl_vat'])
            pop.update_price(code, new_price)
            flash("Price updated successfully!", "success")
            return redirect(url_for('view_stock'))
        accessory = next((acc for acc in pop.read_accessories_from_file() if acc['code'] == code), None)
        return render_template('update_price.html', accessory=accessory)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)