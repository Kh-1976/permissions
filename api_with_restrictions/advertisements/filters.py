from django_filters import rest_framework as filters
from .models import Advertisement
from django_filters.rest_framework import DateFromToRangeFilter


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    filterset_fields = ["creator", "status"]
    search_fields = ["creator", "status"]
    ordering_fields = ["creator", "status"]

    class Meta:
        model = Advertisement
        fields = ["creator", "status"]


class DateFromToRange(filters.FilterSet):
    date_fields = ["created_at"]
    created_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ["created_at"]


