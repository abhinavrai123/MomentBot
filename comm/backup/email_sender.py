import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
email = "abhinavrai123@gmail.com"

def send_email(to_email: str, subject: str, body: str):
    from_email = email
    password = "dmvg jxag zimk hcwo"  # Use an app-specific password from Gmail

    # Create message
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))  # Plaintext version

    try:
        # Connect to Gmail SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

