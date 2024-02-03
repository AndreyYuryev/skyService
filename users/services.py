from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.core.mail import send_mail
from django.conf import settings


class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


def send_email_by_django(subject='', message='', recipients=[]):
    send_mail(subject=subject, message=message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=recipients)
