from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django_rq import job


@job
def send_verification_email(base_url, user):
    token = user.token.key
    verification_link = f'{base_url}api/auth/verify-email/{token}'

    email_body = render_to_string(
        'accounts/email_verification.html',
        {
            'user': user,
            'verification_link': verification_link,
        },
    )

    email = EmailMessage(
        subject='Verify Your Email Address',
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send()
