import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import serial
import time
import warnings
import requests  # For ThingSpeak
import smtplib
import warnings

from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


subject = "= Alert =- "

sender_email = "embedded44@gmail.com"
receiver_emails = ["nareshkanchupati777@gmail.com"]
sender_password = "alqplnjlmgbyoxst"

smtp_server = "smtp.gmail.com"
smtp_port = 587
duration = 5
start_time = time.time()


body1 = "CO Carbon monoxide Gas detected."
body2 = "CO2 Carbon dioxide Gas detected.."
body3 = "Abnormal temperature detected."


api_key = 'H1KAQ9287GN827XZ'
channel_id = '2805455'
warnings.filterwarnings("ignore")
# Base URL for ThingSpeak API
base_url = f'https://api.thingspeak.com/channels/2805455/feeds.json?api_key=TONLUL48MFV1DUOF&results=1'

# Load data from an Excel sheet and split into features and labels
data = pd.read_excel("tk15009.xlsx", engine="openpyxl")

feature_1 = data[['field1']]
feature_2 = data[['field2']]
feature_3 = data[['field3']]


label_1 = data['label_field1']
label_2 = data['label_field2']
label_3 = data['label_field3']



# Split the data into training and testing sets for each parameter
X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(feature_1, label_1, test_size=0.2, random_state=42)
X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(feature_2, label_2, test_size=0.2, random_state=42)
X_train_3, X_test_3, y_train_3, y_test_3 = train_test_split(feature_3, label_3, test_size=0.2, random_state=42)

# Build Random Forest models for each parameter
model_1 = RandomForestClassifier(random_state=42)
model_1.fit(X_train_1, y_train_1)


model_2 = RandomForestClassifier(random_state=42)
model_2.fit(X_train_2, y_train_2)

model_3 = RandomForestClassifier(random_state=42)
model_3.fit(X_train_3, y_train_3)


def send_email(sender_email, receiver_emails, subject, body, smtp_server, smtp_port, sender_password):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Establish a connection to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)  # Log in to the SMTP server
            server.sendmail(sender_email, receiver_emails, msg.as_string())  # Send the email

        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")



def get_thingspeak_data():
    

        response = requests.get(base_url)
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            feeds = data['feeds']
            for feed in feeds:
                # Access each field value
                field1 = feed['field1']
                field2 = feed['field2']
                field3 = feed['field3']
                field4 = feed['field4']
                # Continue for other fields if necessary
                print(f"Field1: {field1}, Field2: {field2}, Field3: {field3}, Field4: {field4}")
                return field1, field2, field3, field4 



while True:
    field1, field2, field3, field4 = get_thingspeak_data()
    time.sleep(1)

   

    x_prediction = model_1.predict([[field1]])[0]
    z_prediction = model_2.predict([[field2]])[0]
    w_prediction = model_3.predict([[field3]])[0]

    print("\nPredictions:")
    print(f'X Prediction: {x_prediction}')
    print(f'Z Prediction: {z_prediction}')
    print(f'Z Prediction: {w_prediction}')
     
    if x_prediction == 1:
        print("CO Carbon monoxide Gas detected.")
        send_email(sender_email, receiver_emails, subject, body1, smtp_server, smtp_port, sender_password)

    else:
        print("No CO Gases Detected")

    if z_prediction == 1:
        print("CO2 Carbon dioxide Gas detected.")
        send_email(sender_email, receiver_emails, subject, body2, smtp_server, smtp_port, sender_password)

    else:
        print("no CO2  is detected")
    if w_prediction == 1:
        print("Abnormal temperature detected")
        send_email(sender_email, receiver_emails, subject, body3, smtp_server, smtp_port, sender_password)

    else:
        print("Temperature is normal")   

    values_string = f"t{x_prediction:.0f}u{z_prediction:.0f}v{w_prediction:.0f}x "
    time.sleep(2)
    print(values_string)
    time.sleep(3)
    
    time.sleep(3)
    print("Completed")
    time.sleep(15)
