from email.message import EmailMessage
from sqlmodel import Session
from database_directory.crud.user_management import get_account_information
import smtplib
import ssl
import os
from jinja2 import Template

email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")
website_url = "https://row-report.onrender.com"

def send_telemetry_email(boat_data: dict, user_id: int, session_id: int, session: Session):
    # Fetch user email and name from the database
    user = get_account_information(session, user_id)
    coach = get_account_information(session, boat_data.get('coach_id'))

    subject = 'RowReport - Telemetry Upload Confirmation'
    email_reciever = user.email

    msg = EmailMessage()
    msg['From'] = f"RowReport <{email_sender}>"
    msg['To'] = email_reciever
    msg['Subject'] = subject

    # Load HTML template
    with open("email_templates/session_email_template.html", "r", encoding="utf-8") as f:
        template = Template(f.read())

    html_content = template.render(
        first_name=user.first_name,
        coach_name=f"{coach.first_name} {coach.last_name}",
        title=boat_data.get("title"),
        description=boat_data.get("description"),
        date=boat_data.get("date"),
        state=boat_data.get("state"),
        serial=boat_data.get("serial"),
        duration=boat_data.get("timeelapsed"),
        distance=boat_data.get("distance"),
        session_id=session_id,
        website_url=website_url
    )

    msg.add_alternative(html_content, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(msg)

def send_account_confirmation_email(account_email: str, first_name: str, account_password: str, account_id: int):
    subject = 'RowReport - Account Confirmation'
    email_reciever = account_email

    msg = EmailMessage()
    msg['From'] = f"RowReport <{email_sender}>"
    msg['To'] = email_reciever
    msg['Subject'] = subject

    # Load HTML template
    with open("email_templates/account_confirmation_template.html", "r", encoding="utf-8") as f:
        template = Template(f.read())

    html_content = template.render(
        first_name=first_name,
        email=account_email,
        password=account_password,
        id=account_id,
        website_url=website_url
    )

    msg.add_alternative(html_content, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(msg)
