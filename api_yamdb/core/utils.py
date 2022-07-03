import json
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage

User = get_user_model()


class EmailSender:
    def __init__(self, request):
        self.current_site = get_current_site(request)

    def get_code_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh)

    def send_token_for_mail(self, email, confirmation_code):
        message = json.dumps({
            'domain': self.current_site.domain,
            'confirmation_code': confirmation_code,
        })
        email = EmailMessage(message, to=[email])
        try:
            email.send()
        except Exception as error:
            raise error
