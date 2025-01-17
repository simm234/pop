# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

# Flask app setup
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key for session management

# File to store accessories
data_file = "pop.txt"

def read_accessories_from_file(filename):
    if not os.path.exists(filename):
        return []  # Return empty list if file does not exist
    with open(filename, 'r') as file:
        try:
            return json.load(file)  # Load accessories as a list of dictionaries
        except json.JSONDecodeError:
            return []  # Return empty list if JSON decoding fails

def write_accessories_to_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'guest' and password == 'guest':
            session['user'] = 'guest'
            return redirect(url_for('view_stock'))
        elif username == 'admin' and password == 'admin123':
            session['user'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' in session and session['user'] == 'admin':
        return render_template('admin_dashboard.html')
    return redirect(url_for('login'))

@app.route('/view_stock')
def view_stock():
    if 'user' in session:
        accessories = read_accessories_from_file(data_file)
        return render_template('view_stock.html', accessories=accessories)
    return redirect(url_for('login'))

@app.route('/add_items', methods=['GET', 'POST'])
def add_items():
    if 'user' in session and session['user'] == 'admin':
        if request.method == 'POST':
            new_item = {
                'name': request.form['name'],
                'code': request.form['code'],
                'description': request.form['description'],
                'remaining_items': int(request.form['remaining_items']),
                'price_excl_vat': float(request.form['price_excl_vat']),
                'price_incl_vat': round(float(request.form['price_excl_vat']) * 1.15, 2)
            }
            accessories = read_accessories_from_file(data_file)
            accessories.append(new_item)
            write_accessories_to_file(data_file, accessories)
            flash('Item added successfully!', 'success')
            return redirect(url_for('view_stock'))
        return render_template('add_items.html')
    return redirect(url_for('login'))

@app.route('/delete_item', methods=['GET', 'POST'])
def delete_item():
    if 'user' in session and session['user'] == 'admin':
        if request.method == 'POST':
            code = request.form['code']
            accessories = read_accessories_from_file(data_file)
            accessories = [item for item in accessories if item['code'] != code]
            write_accessories_to_file(data_file, accessories)
            flash(f"Item with code '{code}' deleted successfully!", 'success')
            return redirect(url_for('view_stock'))
        return render_template('delete_item.html')
    return redirect(url_for('login'))

@app.route('/update_price', methods=['GET', 'POST'])
def update_price():
    if 'user' in session and session['user'] == 'admin':
        if request.method == 'POST':
            code = request.form['code']
            new_price = float(request.form['price_excl_vat'])
            accessories = read_accessories_from_file(data_file)
            for item in accessories:
                if item['code'] == code:
                    item['price_excl_vat'] = new_price
                    item['price_incl_vat'] = round(new_price * 1.15, 2)
                    break
            write_accessories_to_file(data_file, accessories)
            flash(f"Price for item with code '{code}' updated successfully!", 'success')
            return redirect(url_for('view_stock'))
        return render_template('update_price.html')
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
        total_price = quantity * item['price_incl_vat']

        # Step 1: Check if enough stock is available
        if item['remaining_items'] >= quantity:
            # Step 2: Update stock after purchase
            item['remaining_items'] -= quantity
            write_accessories_to_file('pop.txt', accessories)  # Update pop.txt with the new stock

            # Step 3: Log the purchase to selled.txt
            with open('selled.txt', 'a') as file:
                purchase_data = {
                    'name': item['name'],
                    'code': item['code'],
                    'quantity': quantity,
                    'price_incl_vat': item['price_incl_vat'],
                    'total_price': total_price,
                }
                file.write(json.dumps(purchase_data) + '\n')  # Append the purchase data to selled.txt

            # Step 4: Return the confirmation page with the purchase details
            return render_template('confirmation.html', item=item, quantity=quantity, total_price=total_price)
        else:
            flash("Not enough stock available.", "error")
            return redirect(url_for('view_stock'))

    return render_template('buy_now.html', item=item)

@app.route('/selled_items')
def selled_items():
    if 'user' in session and session['user'] == 'admin':
        try:
            with open('selled.txt', 'r') as file:
                selled_items = [json.loads(line) for line in file.readlines()]
        except (FileNotFoundError, json.JSONDecodeError):
            selled_items = []

        return render_template('selled_items.html', selled_items=selled_items)

    return redirect(url_for('login'))


@app.route('/buy_selected', methods=['GET', 'POST'])
def buy_selected():
    filename = "pop.txt"
    if request.method == 'POST':
        selected_items = request.form.getlist('selected_items')  # List of selected item codes
        total_price = 0

        # Step 1: Read existing accessories from the file
        accessories = read_accessories_from_file(filename)

        # Step 2: Update stock and calculate total price
        selled_items = []
        for item in accessories:
            if item['code'] in selected_items:
                quantity = int(request.form[f'quantity_{item["code"]}'])
                if item['remaining_items'] >= quantity:
                    total_price += item['price_incl_vat'] * quantity
                    item['remaining_items'] -= quantity  # Decrease stock

                    # Add to selled_items for logging
                    selled_items.append({
                        'name': item['name'],
                        'code': item['code'],
                        'quantity': quantity,
                        'price_incl_vat': item['price_incl_vat'],
                        'total_price': item['price_incl_vat'] * quantity,
                    })
                else:
                    flash(f"Not enough stock for item {item['code']}.", "error")
                    return redirect(url_for('view_stock'))

        # Step 3: Update the file with new stock information
        write_accessories_to_file(filename, accessories)

        # Step 4: Return the order confirmation or a similar response
        flash(f"Total price for selected items: {total_price:.2f}", "success")
        return render_template('confirmation.html', selled_items=selled_items, total_price=total_price)
    
    # If the method is GET, return the page with a form (if necessary)
    return render_template('buy_selected.html')

if __name__ == '__main__':
    if not os.path.exists(data_file):
        write_accessories_to_file(data_file, [])
    app.run(debug=True)