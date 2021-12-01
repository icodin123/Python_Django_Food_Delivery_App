from django.template.loader import render_to_string
from homepage.settings import *
from django.core import mail

def send_email(receiver, message, subject, html_template=None, link=None):
    """Send email to a receiver, html_template is a string name of html template file."""

    receivers = [receiver]
    if html_template:
        html = render_to_string(html_template, {'message': message, 'link': link})
        mail.send_mail(subject, message, EMAIL_HOST_USER, receivers, html_message=html)

    mail.send_mail(subject, message, EMAIL_HOST_USER, receivers)
