from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os
from flask_otp import OTP
from otp_secret import OTPSecret  # Importer OTPSecret depuis un fichier otp_secret.py
import pyotp
import qrcode
from pyotp import TOTP
from io import BytesIO
import base64
from config import Config
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)
config_instance = Config()

data = pd.read_csv(config_instance.mydata, encoding='ISO-8859-1')  # Replace 'ISO-8859-1' with the appropriate encoding
app.secret_key = os.urandom(24)
app.config['OTP_SECRET'] = OTPSecret()
otp = OTP(app)


# Database Configuration
db = mysql.connector.connect(
    host='localhost',
    user= config_instance.user,
    password= config_instance.password,
    database=config_instance.database
)
cursor = db.cursor(buffered=True)

@app.route('/map')
def map():
    # Pass location data to the template
    return render_template('map.html', data=data)

@app.route('/')
def register():
    return render_template('register.html')


# Routes
@app.route('/login2', methods=['POST'])
def login2():
    entered_username = request.form['username']
    entered_password = request.form['password']

    # Query to check credentials in the database
    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(sql, (entered_username, entered_password))
    user = cursor.fetchone()

    if user:
        username = user[1]
        password = user[2]

        # If user exists in the database, redirect to OTP verification
        session['username'] = username
        session['password'] = password

        return render_template('verify_otp.html', username=username)  # Page de vérification de l'OTP
    else:
        return "Invalid credentials. Please try again."

@app.route('/verify', methods=['POST'])
def verify():
    entered_otp = request.form['otp']
    username = session.get('username')
    qr_code_otp = request.form['qr_code_otp']

    if username:
        # Fetch the OTP secret for the user from the database
        sql = "SELECT otp_secret FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        otp_secret = cursor.fetchone()
        #otp_secret = cursor.fetchall()

        otp_secret = otp_secret[0] 
        cleaned_fetched_otp = otp_secret.replace("(", "").replace(")", "").replace(",", "").replace(" ", "")

        if cleaned_fetched_otp == entered_otp :
            if qr_code_otp:
                    # Create TOTP object using fetched OTP secret for the QR code OTP verification
                    totp_qr = TOTP(otp_secret)

                    # Verify the OTP from Google Authenticator
                    if totp_qr.verify(qr_code_otp):
                        # Both OTP verifications successful
                        return redirect('/map')
                    else:
                        # Invalid QR code OTP
                        return "Invalid QR Code OTP. Please try again."
            else:
                # QR code OTP not provided
                return "Please provide QR Code OTP."

            return redirect('/weather')
        else: return "Invalid OTP. Please try again."
    else:
        return "User not logged in. Please log in first."



@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/register2', methods=['POST'])
def register2():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Generate an OTP secret for the user
        otp_secret = pyotp.random_base32()

        # Insert new user into the database with OTP secret
        query = "INSERT INTO users (username, password, otp_secret) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, otp_secret))
        db.commit()

        # Create an OTP URI for the QR code
        otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(username, issuer_name="YourAppName")


        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(otp_uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Display the QR code in the save_otp.html template
        buffered = BytesIO()
        img.save(buffered)
        buffered.seek(0)

        qr_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return render_template('save_otp.html', qr_image=qr_image, otp_secret=otp_secret)
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
