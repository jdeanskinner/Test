from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection configuration
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='webuser',           # Your DB username
        password='webpassword',   # Your DB password
        database='webserver_test' # The database name
    )

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO submissions (name, email, message) VALUES (%s, %s, %s)",
                           (name, email, message))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('home'))

        except Error as e:
            print(f"Error: {e}")
            return 'Database error. Please try again later.'
    return 'Invalid request method.'

if __name__ == '__main__':
    app.run(debug=True)
