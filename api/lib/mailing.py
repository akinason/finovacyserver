import random
from django.core.mail import send_mail

from finovacyserver import settings


def send_password_set_or_reset_email(email, borrower_name=''):
    code = random.randint(57521, 99861)
    subject = "Finovacy Account Password Reset"
    message = "Hello \nPlease enter the following code to set or reset your password {code}".format(code=code)
    html_message = "<h3>Hello {first_name}</h3><p>Please enter the following code to set " \
                   "or reset your password</p><br><h1>{code}</h1><br><br><p>Best Regards</p>".format(
                    first_name=borrower_name, code=code
                    )
    res = send_mail(
        subject=subject, message=message,
        from_email="Finovacy <{from_email}>".format(from_email=settings.DEFAULT_FROM_EMAIL), recipient_list=[email],
        html_message=html_message
    )
    return {"response": res, "code": code}

