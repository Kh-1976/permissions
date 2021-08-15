from django_filters import rest_framework as filters
from .models import Advertisement
from django_filters.rest_framework import DateFromToRangeFilter


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    filterset_fields = ["creator"]
    search_fields = ["creator"]
    ordering_fields = ["creator"]

    class Meta:
        model = Advertisement
        fields = ["creator"]

class DateFromToRange(filters.FilterSet):
    data_fields = ["created_at"]
    created_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ["created_at"]


