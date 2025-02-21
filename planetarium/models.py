from django.db import models
from django.contrib.auth.models import User


class AstronomyShow(models.Model):
    title = models.CharField(
        max_length=255,
        null=True,
    )
    description = models.TextField()

    def __str__(self):
        return self.title


class ShowTheme(models.Model):
    name = models.CharField(
        max_length=255
    )
    astronomy_shows = models.ManyToManyField(
        AstronomyShow,
        related_name="themes"
    )

    def __str__(self):
        return self.name


class PlanetariumDome(models.Model):
    name = models.CharField(
        max_length=255
    )
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        AstronomyShow,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    planetarium_dome = models.ForeignKey(
        PlanetariumDome,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.astronomy_show.title} at {self.show_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    def __str__(self):
        return f"Reservation {self.id} by {self.user.username}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    show_session = models.ForeignKey(
        ShowSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        unique_together = (
            "show_session",
            "row",
            "seat"
        )

    def __str__(self):
        return (
            f"Ticket {self.id}: "
            f"{self.row}-{self.seat} for "
            f"{self.show_session}"
        )
