from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Advertisement
from .serializers import AdvertisementSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .filters import AdvertisementFilter, DateFromToRange
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    search_fields = AdvertisementFilter.search_fields
    ordering_fields = AdvertisementFilter.ordering_fields
    pagination_class = PageNumberPagination
    data_fields = DateFromToRange.data_fields

    def destroy(self, request, *args, **kwargs):
        queryset_del = Advertisement.objects.all()
        instance = self.get_object()
        data = [{"id": q.id, "creator": q.creator} for q in queryset_del]
        for i in data:
            if i["id"] == instance.pk and i["creator"] == self.request.user:
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        queryset_upd = Advertisement.objects.all()
        queryset_obj = self.get_object()
        instance = self.get_object()
        data = request.data
        data_q = [{"id": q.id, "creator": q.creator} for q in queryset_upd]
        for i in data_q:
            if i["id"] == instance.pk and i["creator"] == self.request.user:
                queryset_obj.status = data.get("status", queryset_obj.status)
                queryset_obj.save()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_permissions(self):
        """Получение прав для действий."""
        for k in self.request.GET.keys():
            key = k
        if len(self.request.GET) != 0:
            if key == 'creator':
                self.filterset_fields = AdvertisementFilter.filterset_fields
            elif key == 'created_at_after' or key == 'created_at_before':
                self.filter_class = DateFromToRange

        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        return []


