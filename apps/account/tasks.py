from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_confirm_email(user, verification_code):
    subject = 'Registration confirmation'
    
    context = {
        'user': user,
        'verification_code': verification_code,
        'support_email': settings.SUPPORT_EMAIL
    }

    text_content = render_to_string('email/confirmation_email.txt', context)
    html_content = render_to_string('email/confirmation_email.html', context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
        reply_to=settings.SUPPORT_EMAIL
    )
    email.attach_alternative(html_content, "text/html")
    email.send()