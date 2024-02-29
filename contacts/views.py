"""
Views for the contact app.
"""

from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from rest_framework.decorators import api_view
from rest_framework.response import Response


def send_custom_email(subject, message):
    """
    This function is used to send an email from the contact form using standard django emails.
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [settings.CONTACT_FORM_RECIPIENT_EMAIL],
        fail_silently=False,
    )


def send_confirmation_email_to_sender(sender):
    """
    This function is used to email the sender of the contact form.
    """
    subject = "Conferma invio messaggio"
    message = (
        f"Grazie per averci contattato, {sender}!\n"
        "Ti risponderemo il prima possibile."
    )
    send_mail(subject, message, settings.EMAIL_HOST_USER, [sender], fail_silently=False)


@api_view(["POST"])
def contacts_form_view(request):
    """
    This view is used to send an email from the contact form.
    """
    try:
        name = strip_tags(request.data["name"])
        surname = strip_tags(request.data["surname"])
        email = strip_tags(request.data["email"])
        subject = strip_tags(request.data["subject"])
        message = strip_tags(request.data["message"])

        try:
            send_confirmation_email_to_sender(email)
        except Exception:
            return Response({"status": "error_confirmation_email"})

        final_message = (
            f"EMAIL: {email}\n"
            f"NOME: {name}\n"
            f"COGNOME: {surname}\n"
            f"\n\nMESSAGGIO:\n"
            f"{message}"
        )

        send_custom_email(subject, final_message)
        return Response({"status": "ok"})
    except Exception as e:
        return Response({"status": "error"})
