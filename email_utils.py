import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
load_dotenv()

EMAIL_PASSWORD = os.environ.get("GOOGLE_EMAIL_PASSWORD")
EMAIL_USERNAME = os.environ.get("GOOGLE_EMAIL_USERNAME")

def send_email(body_template_name, to_email, subject, email_values):
    try:
        env = Environment(loader=FileSystemLoader('data/email_templates'))
        template = env.get_template(body_template_name, )
        html_message = template.render(email_values)
        
        # Create a MIMEText object for the HTML message
        email_body = MIMEMultipart('alternative')
        email_body['From'] = EMAIL_USERNAME
        email_body['To'] = to_email
        email_body['Subject'] = subject

        # Attach the HTML message to the email body
        email_body.attach(MIMEText(html_message, 'html'))

        # Create an SMTP client session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

        # Send the email
        server.sendmail(EMAIL_USERNAME, to_email, email_body.as_string())

        print('HTML email sent successfully!')
    except Exception as e:
        print(f'An error occurred: {str(e)}')
    finally:
        server.quit()