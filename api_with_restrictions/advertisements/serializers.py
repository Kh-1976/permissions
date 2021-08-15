from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""
        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        queryset = Advertisement.objects.all()
        queryset_data = [{"creator": q.creator, "status": q.status} for q in queryset]
        count_status = 0
        for i in queryset_data:
            if i["creator"] == self.context["request"].user and i["status"] == "OPEN":
                count_status += 1
        """Метод для валидации. Вызывается при создании и обновлении."""
        # TODO: добавьте требуемую валидацию
        if count_status >= 10:
           raise ValidationError()

        return data

