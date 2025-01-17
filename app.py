from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
from pop import delete_accessory
import pop
import os
from pop import write_accessories_to_file, read_accessories_from_file

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

@app.route('/buy_selected', methods=['GET', 'POST'])
def buy_selected():
    filename = "pop.txt"
    if request.method == 'POST':
        selected_items = request.form.getlist('selected_items')  # List of selected item codes
        total_price = 0
        accessories = read_accessories_from_file(filename)

        # Update stock and calculate total price
        for item in accessories:
            if isinstance(item, CarAccessory) and item.to_dict()['code'] in selected_items:
                quantity = int(request.form[f'quantity_{item.to_dict()["code"]}'])
                total_price += item._CarAccessory__price_incl_vat * quantity
                item._CarAccessory__remaining_items -= quantity  # Decrease stock

        write_accessories_to_file(filename, accessories)

        return render_template('buy_selected.html', accessories=accessories, total_price=total_price)

    else:
        # Handle GET request, show items
        accessories = read_accessories_from_file(filename)
        return render_template('buy_selected.html', accessories=accessories, total_price=0)


@app.route('/sell_selected', methods=['POST'])
def sell_selected():
    selected_items = request.form.getlist('selected_items')
    quantities = {}
    total_price = 0
    filename = "pop.txt" 
    # Loop through selected items and their corresponding quantities
    for item_code in selected_items:
        quantity_key = f"quantity_{item_code}"
        quantity = int(request.form.get(quantity_key, 1))  # Default to 1 if not provided

        # Check if stock is sufficient for selling
        accessory = next((acc for acc in pop.read_accessories_from_file(filename) if acc.to_dict()['code'] == item_code), None)
        if accessory and accessory.to_dict()['remaining_items'] > 1 and quantity <= 100:
            quantities[item_code] = quantity
            total_price += accessory.to_dict()['price_incl_vat'] * quantity  # Add to total price
            # Increase the stock (selling means we increase the stock in the system)
            accessory._CarAccessory__remaining_items += quantity

    # Write the updated accessories list back to the file
    pop.write_accessories_to_file(filename, pop.read_accessories_from_file(filename))

    # Display the total price and render the confirmation page
    return render_template('sell_now.html', quantities=quantities, total_price=total_price)

    
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
    if 'user' in session and session['user'] == 'admin':
        if request.method == 'POST':
            code = request.form['code']
            accessories = read_accessories_from_file('pop.txt')

            accessory_exists = any(acc['code'] == code for acc in accessories)

            if accessory_exists:
                # Filter out the accessory with the given code
                filtered_accessories = [acc for acc in accessories if acc['code'] != code]
                write_accessories_to_file('pop.txt', filtered_accessories)
                flash(f"Accessory with code '{code}' deleted successfully!", "success")
            else:
                flash(f"No accessory found with code '{code}'.", "error")

            return redirect(url_for('delete_item'))
        return render_template('delete_item.html')
    return redirect(url_for('login'))

@app.route('/update_price', methods=['GET', 'POST'])
def update_price():
    if 'user' in session and session['user'] == 'admin':
        if request.method == 'POST':
            code = request.form['code']
            new_price = float(request.form['price_excl_vat'])
            # Call the update function with the provided code and price
            pop.update_price(code, new_price)
            flash("Price updated successfully!", "success")
            return redirect(url_for('view_stock'))
        return render_template('update_price.html')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)