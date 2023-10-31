import smtplib, ssl
from news_email_sender.news_api import serve_info
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import os
# Variables
port = 465  # For SSL
password = os.getenv('PASSWORD')
to_addr = "0220120362@harrowschool.hk"
from_addr = "marcoleepython@gmail.com"


# Set up the Jinja2 environment and load the template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('news_email_sender/email_temp.html')

# Retrieve news
news_dict = serve_info()

# Render the template with your news data
html_body = template.render(news_items=news_dict)


# Create a secure SSL context
context = ssl.create_default_context()

# Create a MIME multipart object
msg = MIMEMultipart()

# Set email headers
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = 'Daily news feed'

# Attach the HTML body to the email
html_part = MIMEText(html_body, 'html')
msg.attach(html_part)

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(from_addr, password)
    server.sendmail(
        from_addr=from_addr,
        to_addrs=to_addr,
        msg=msg.as_string()
        )

