from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use Gmail's SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Your email address
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Your email password or app password
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
mail = Mail(app)

# Home Route - About Page
@app.route('/')
def index():
    return render_template('index.html')

# Contact Page Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Send email using Flask-Mail
        msg = Message('New Contact Form Submission',
                      recipients=[os.getenv('RECEIVER_EMAIL')])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        try:
            mail.send(msg)
            return redirect(url_for('thank_you'))
        except Exception as e:
            return f"Error: {str(e)}"
    
    return render_template('contact.html')

# Thank You Page Route after form submission
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

# Projects Page Route
@app.route('/projects')
def projects():
    return render_template('projects.html')

if __name__ == '__main__':
    app.run(debug=True)
