import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = "REDACTED"
EMAIL_PASSWORD = "REDACTED"

def send_email(msg):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# sending an email to admin when a new user signs up
def email_admin_new_signup(user):
    msg = EmailMessage()
    msg['Subject'] = "New SignUp from {} {}".format(user.first_name, user.last_name)
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content("New user with following information has signed up\n"
                    "\tfirst_name : {}\n"
                    "\tlast_name : {}\n"
                    "\temail: {}".format(user.first_name, user.last_name, user.email))
    send_email(msg)

# sending an email to new user when they sign up
def email_user_new_signup(user):
    msg = EmailMessage()
    msg['Subject'] = "Thanks for Signing Up {} {}".format(user.first_name, user.last_name)
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = user.email
    msg.set_content("You have signed up with following information\n"
                    "\tfirst_name : {}\n"
                    "\tlast_name : {}\n"
                    "\temail: {}".format(user.first_name, user.last_name, user.email))
    send_email(msg)

def email_admin_new_request(request):
    msg = EmailMessage()
    msg['Subject'] = "New Request from {} {}".format(request.user_id.first_name, request.user_id.last_name)
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content("User:\n"
                    "\tfirst_name : {}\n"
                    "\tlast_name : {}\n"
                    "\temail: {}\n"
                    "Has made following request:\n"
                    "\tRequest Type: {}\n"
                    "\tRequest: {}\n"
                    .format(request.user_id.first_name, request.user_id.last_name, request.user_id.email, request.get_type(), request.request_change))
    send_email(msg)

def email_user_new_request(request):
    msg = EmailMessage()
    msg['Subject'] = "We have received your request".format(request.user_id.first_name, request.user_id.last_name)
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = request.user_id.email
    msg.set_content("Your request:\n"
                    "\tRequest Type: {}\n"
                    "\tRequest: {}\n"
                    .format(request.get_type(), request.request_change))
    send_email(msg)

def email_admin_new_application(app_review):
    msg = EmailMessage()
    msg['Subject'] = "New application from {} {}".format(app_review.model_id.first_name, app_review.model_id.last_name)
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content("User:\n"
                    "\tFirst Name: {}\n"
                    "\tLast Name: {}\n"
                    "\tEmail: {}"
                    "Has made a new application:\n"
                    "\tApplication Type: {}\n"
                    "\tComments: {}\n"
                    .format(app_review.model_id.first_name, app_review.model_id.last_name, app_review.model_id.email,\
                            app_review.get_type(), app_review.comments))
    send_email(msg)

def email_user_new_application(app_review):
    msg = EmailMessage()
    msg['Subject'] = "We have received your application".format(app_review.model_id.first_name, app_review.model_id.last_name)
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = app_review.model_id.email
    msg.set_content("{} {} thanks for showing interest in working with Feeding Canadian Kids. We have received your "
                    "application and we will contact you shortly\n "
                    "\tApplication Type: {}\n"
                    "\tComments: {}\n"
                    .format(app_review.model_id.first_name, app_review.model_id.last_name, app_review.get_type(),\
                            app_review.comments))
    send_email(msg)
