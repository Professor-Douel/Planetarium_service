from rest_framework import (
    viewsets,
    filters,
    permissions
)
from rest_framework_simplejwt.authentication import JWTAuthentication

from planetarium.models import (
    AstronomyShow,
    ShowTheme,
    PlanetariumDome,
    ShowSession,
    Reservation
)

from planetarium.serializers import (
    AstronomyShowSerializer,
    ShowThemeSerializer,
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    ReservationSerializer
)


class BaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]


class AstronomyShowViewSet(BaseViewSet):
    queryset = AstronomyShow.objects.prefetch_related("themes").all()
    serializer_class = AstronomyShowSerializer
    search_fields = [
        "title",
        "description"
    ]
    ordering_fields = [
        "id",
        "title"
    ]


class ShowThemeViewSet(BaseViewSet):
    queryset = ShowTheme.objects.prefetch_related("astronomy_shows").all()
    serializer_class = ShowThemeSerializer
    search_fields = ["name"]
    ordering_fields = [
        "id",
        "name"
    ]


class PlanetariumDomeViewSet(BaseViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    search_fields = ["name"]
    ordering_fields = [
        "id",
        "name",
        "rows",
        "seats_in_row"
    ]


class ShowSessionViewSet(BaseViewSet):
    queryset = ShowSession.objects.select_related(
        "astronomy_show",
        "planetarium_dome"
    ).all()
    serializer_class = ShowSessionSerializer
    search_fields = [
        "astronomy_show__title",
        "planetarium_dome__name"
    ]
    ordering_fields = [
        "id",
        "show_time"
    ]


class ReservationViewSet(BaseViewSet):
    queryset = Reservation.objects.select_related(
        "user"
    ).prefetch_related(
        "tickets"
    ).all()
    serializer_class = ReservationSerializer
    ordering_fields = [
        "id",
        "created_at"
    ]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
