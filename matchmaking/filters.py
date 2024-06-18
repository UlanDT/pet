"""Module containing deal filtering configs."""
import django_filters

from matchmaking.models import Deal


class DealFilter(django_filters.FilterSet):
    """Filter deals by status."""

    status = django_filters.CharFilter(field_name="status")

    class Meta:
        """Meta class."""

        model = Deal
        fields = (
            "status",
        )
