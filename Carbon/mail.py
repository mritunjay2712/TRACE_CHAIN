import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set your email credentials
my_email = "whitedevil1481@gmail.com"
my_password = "qwerty1234&4321"

# Set up the SMTP connection
try:
    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(user=my_email, password=my_password)

    # Compose the message
    msg = MIMEMultipart()
    msg['From'] = my_email
    msg['To'] = "mritunjaysingh1481@gmail.com"
    msg['Subject'] = "Subscription request"
    body = "Subscribe"
    msg.attach(MIMEText(body, 'plain'))

    # Send the message
    connection.send_message(msg)

    # Close the connection
    connection.quit()
    print("Email sent successfully")

except smtplib.SMTPAuthenticationError:
    print("Authentication Error: Please check your email and password.")
except smtplib.SMTPException as e:
    print("SMTP Exception: ", e)
except Exception as e:
    print("An unexpected error occurred: ", e)
