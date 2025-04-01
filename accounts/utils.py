from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_otp_email(user, otp_code):
    """Send OTP code to user's email"""
    subject = 'Your OTP Code for Login'
    html_message = render_to_string('accounts/email/otp_email.html', {
        'user': user,
        'otp_code': otp_code
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )