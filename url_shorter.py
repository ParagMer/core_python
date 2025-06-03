import sqlite3
import hashlib
import string
import random
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
DB_NAME = 'url_shortener.db'


def init_db():
    """Initialize the database and create the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            short_url TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()


def generate_short_url(long_url):
    """Generate a unique short URL using hashing."""
    hash_object = hashlib.md5(long_url.encode())
    short_hash = hash_object.hexdigest()[:6]  # Get the first 6 characters
    return short_hash


def save_url(long_url, short_url):
    """Save the long URL and its corresponding short URL to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO urls (long_url, short_url) VALUES (?, ?)
    ''', (long_url, short_url))
    conn.commit()
    conn.close()


def get_long_url(short_url):
    """Retrieve the long URL based on the short URL."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT long_url FROM urls WHERE short_url = ?
    ''', (short_url,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


@app.route('/')
def home():
    """Render the home page with the form to shorten URLs."""
    return render_template_string('''
        <form method="POST" action="/shorten">
            <label for="url">Enter URL to shorten:</label>
            <input type="text" name="url" id="url" required>
            <button type="submit">Shorten</button>
        </form>
    ''')


@app.route('/shorten', methods=['POST'])
def shorten():
    """Generate the short URL and save it in the database."""
    long_url = request.form['url']
    short_url = generate_short_url(long_url)
    save_url(long_url, short_url)
    return render_template_string('''
        <h3>Shortened URL:</h3>
        <p>Short URL: <a href="/{{ short_url }}">{{ short_url }}</a></p>
        <p>Original URL: {{ long_url }}</p>
        <a href="/">Go back</a>
    ''', short_url=short_url, long_url=long_url)


@app.route('/<short_url>')
def redirect_to_url(short_url):
    """Redirect to the long URL based on the short URL."""
    long_url = get_long_url(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found!", 404


if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
