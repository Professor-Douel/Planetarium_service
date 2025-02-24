from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation(user_email, order_details):
    """

    :rtype: object
    """
    subject = "Підтвердження замовлення в Planetarium"
    message = (f"Дякуємо за ваше замовлення!"
               f"Деталі замовлення:"
               f"{order_details}")

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
