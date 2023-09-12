from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'first_name', 'phone', 'email', 'date_joined', 'last_login')
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
        }


class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'first_name', 'email', 'phone', 'date_joined', 'last_login', 'block')


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'phone', 'email')


class SupportPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ('text',)


class AllSupportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = '__all__'

    def to_representation(self, instance):
        support = super().to_representation(instance)
        user_id = support.get('user_fk')
        if user_id:
            user = CustomUser.objects.get(id=user_id)
            user_serializer = CustomUserSerializer(user)
            support['user'] = user_serializer.data
        return support


class AddCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_rasm(self, value):
        allowed_extensions = ('.png', '.jpg', '.jpeg', '.ico')
        if not value.name.lower().endswith(allowed_extensions):
            raise ValidationError("Fayl formati noto'g'ri. Faqat .png, .jpg yoki .jpeg formatlarni qabul qilinadi.")
        return value


class UpdateCategorySerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    rasm = serializers.FileField(required=False)
