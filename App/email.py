from django.conf import settings
from .models import MyUser

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_otp_email(email, otp, user_name):
    subject = "Discord Bot - Password Reset OTP"
    template_path = 'email-verify-otp.html'

    try:
        message = render_to_string(template_path, {'otp': otp,'user_name':user_name })
        msg = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [email])
        msg.attach_alternative(message, "text/html")
        msg.send()
    except Exception as e:
        print("Error: unable to send email:", e)
        return False
    
    return True
