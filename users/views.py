"""
Views for users' app
"""

from django.conf import settings
from django.http import HttpResponseRedirect


def email_confirm_redirect(request, key):
    """
    Redirects to frontend after email confirmation is done
    :param request: Request object
    :param key: Confirmation key
    :return: HttpResponseRedirect to frontend URL
    """
    return HttpResponseRedirect(f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/")


def password_reset_confirm_redirect(request, uidb64, token):
    """
    Redirects to frontend after password reset are done
    :param request: Request object
    :param uidb64: User ID (the one who confirms the password reset)
    :param token: A token to confirm the password reset
    :return: HTTPResponseRedirect to frontend URL
    """
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )
