from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from planetarium.views import (
    AstronomyShowViewSet,
    ShowThemeViewSet,
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    ReservationViewSet,
)


app_name = "planetarium"

router = DefaultRouter()
router.register(r"astronomy-shows", AstronomyShowViewSet)
router.register(r"show-themes", ShowThemeViewSet)
router.register(r"planetarium-domes", PlanetariumDomeViewSet)
router.register(r"show-sessions", ShowSessionViewSet)
router.register(r"reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
