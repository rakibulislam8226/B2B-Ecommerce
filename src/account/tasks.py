from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.urls import reverse
from .models import User


def send_activation_email_async(user_id, domain):
    user = User.objects.get(id=user_id)

    # Generate the activation token
    token_generator = default_token_generator
    token = token_generator.make_token(user)

    # Generate the uidb64 for the user's primary key
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    # Construct the activation link using the provided domain
    activation_url = reverse("activate", kwargs={"uidb64": uidb64, "token": token})
    activation_link = f"http://{domain}{activation_url}"

    # Rest of the code to send the activation email
    mail_subject = "Activate your account"
    message = render_to_string(
        "activation_email.html",
        {
            "user": user,
            "activation_link": activation_link,
        },
    )
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.content_subtype = "html"
    print(f"Activation mail send to {user.email}")
    email.send()
