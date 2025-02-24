from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Reservation


@receiver(post_save, sender=Reservation)
def send_reservation_email(sender, instance, created, **kwargs):
    if created:
        tickets = instance.tickets.all()
        if tickets.exists():
            ticket = tickets.first()
            show_session = ticket.show_session
            astronomy_show = show_session.astronomy_show

            subject = "Ваше бронювання у Планетарії підтверджено!"
            message = (
                f"Дякуємо за бронювання у планетарії!\n\n"
                f"Шоу: {astronomy_show.title}\n"
                f"Дата та час: {show_session.show_time}\n"
                f"Кількість квитків: {tickets.count()}\n\n"
                f"До зустрічі!"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.user.email],
                fail_silently=False,
            )
