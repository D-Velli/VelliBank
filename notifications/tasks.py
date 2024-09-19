from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage


@shared_task
def send_registration_email(client_email, client_mdp, client_name):
    html_content = render_to_string("notifications/register_confirmation.html", {
        "client_email": client_email,
        "client_mdp": client_mdp,
        "client_name": client_name,
    })

    # Version texte brut pour les clients qui ne supportent pas HTML
    text_content = strip_tags(html_content)

    # Sujet et email de l'expéditeur
    subject = "Confirmation de l'ouverture de votre compte bancaire"
    email_from = settings.DEFAULT_FROM_EMAIL

    # Créer l'email avec EmailMultiAlternatives
    msg = EmailMultiAlternatives(subject, text_content, email_from, [client_email])

    # Ajouter le contenu HTML à l'email
    msg.attach_alternative(html_content, "text/html")

    # Attacher l'image inline
    image_path = f'{settings.BASE_DIR / "static" / "logo.png"}'  # Remplace par le chemin de ton image
    print(f"image_path: {image_path}")
    try:
        with open(image_path, 'rb') as f:
            image = MIMEImage(f.read())
            image.add_header('Content-ID', '<logo_image>')
            msg.attach(image)
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'image : {e}")
    # Envoyer l'email
    msg.send()

@shared_task
def send_reset_password_email(client_email, client_mdp, client_name):
    # Charger le template HTML
    html_content = render_to_string("notifications/reset_password.html", {
        "client_email": client_email,
        "client_mdp": client_mdp,
        "client_name": client_name
    })

    # Version texte brut pour les clients qui ne supportent pas HTML
    text_content = strip_tags(html_content)

    subject = "Confirmation de l'ouverture de votre compte bancaire"
    email_from = settings.DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives(subject, text_content, email_from, [client_email])
    msg.attach_alternative(html_content, "text/html")
    image_path = f'{settings.BASE_DIR / "static" / "logo.png"}'
    print(f"image_path: {image_path}")
    try:
        with open(image_path, 'rb') as f:
            image = MIMEImage(f.read())
            image.add_header('Content-ID', '<logo_image>')
            msg.attach(image)
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'image : {e}")
    # Envoyer l'email
    msg.send()
