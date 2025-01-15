from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key for session management

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
        return render_template('view_stock.html')
    return redirect(url_for('login'))

@app.route('/selled_items')
def selled_items():
    if 'user' in session and session['user'] == 'admin':
        return render_template('selled_items.html')
    return redirect(url_for('login'))

@app.route('/delete_items')
def delete_items():
    if 'user' in session and session['user'] == 'admin':
        return render_template('delete_items.html')
    return redirect(url_for('login'))

@app.route('/add_items')
def add_items():
    if 'user' in session and session['user'] == 'admin':
        return render_template('add_items.html')
    return redirect(url_for('login'))

@app.route('/update_price')
def update_price():
    if 'user' in session and session['user'] == 'admin':
        return render_template('update_price.html')
    return redirect(url_for('login'))

@app.route('/view_report')
def view_report():
    if 'user' in session and session['user'] == 'admin':
        return render_template('view_report.html')
    return redirect(url_for('login'))

@app.route('/search')
def search():
    query = request.args.get('query', '')
    # Perform search logic here
    return render_template('search_results.html', query=query)

if __name__ == '__main__':
    app.run(debug=True)
