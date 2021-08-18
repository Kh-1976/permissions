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
    pagination_class = PageNumberPagination

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        permission_delete = bool(Advertisement.objects.filter(creator=self.request.user, id=instance.pk))
        if permission_delete:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response("Неверный токен", status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset_obj = self.get_object()
        data = request.data
        permission_partial_update = bool(Advertisement.objects.filter(creator=self.request.user, id=instance.pk))
        if permission_partial_update:
            queryset_obj.status = data.get("status", queryset_obj.status)
            queryset_obj.title = data.get("title", queryset_obj.title)
            queryset_obj.description = data.get("description", queryset_obj.description)
            queryset_obj.save()
            return Response(status=status.HTTP_200_OK)
        return Response("Неверный токен",status=status.HTTP_404_NOT_FOUND)

    def get_permissions(self):
        for k in self.request.GET.keys():
            key = k
        if len(self.request.GET) != 0:
            if key == "creator" or key == "status":
                self.filterset_fields = AdvertisementFilter.filterset_fields
            elif key == "created_at_after" or key == "created_at_before":
                self.filter_class = DateFromToRange

        if self.action in ["destroy", "create", "update", "partial_update"]:
            return [IsAuthenticated()]
        return []


