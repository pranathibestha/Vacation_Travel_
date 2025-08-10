import smtplib
from email.mime.text import MIMEText

def send_confirmation_email(to, name, place, total):
    sender = "pranathibestha@gmail.com"
    password = "pranathi@123"

    msg = MIMEText(f"""
Hello {name},

Your booking for {place} is successful.
Total amount paid: ₹{total}

Thank you for choosing our planner!

Regards,
Bug Smashers Team
""")
    msg['Subject'] = 'Booking Confirmation - Travel Planner'
    msg['From'] = sender
    msg['To'] = to

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Email sending failed:", e)