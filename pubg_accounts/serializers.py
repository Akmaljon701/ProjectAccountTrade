from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.serializers import *
from .models import *


class PubgAccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PubgAccount
        fields = ('category_fk', 'type', 'price', 'level', 'rp', 'clothes', 'skins', 'titles', 'detail', 'user_fk')
        extra_kwargs = {
            'user_fk': {'read_only': True}
        }


class PubgAccountAddMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PubgAccountMedia
        fields = '__all__'

    def validate_file(self, value):
        allowed_extensions = ('.png', '.jpg', '.jpeg', '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.3gp', '.m4v', '.vob')
        if not value.name.lower().endswith(allowed_extensions):
            raise ValidationError("Fayl formati noto'g'ri. Faqat '('.png', '.jpg', '.jpeg', '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.3gp', '.m4v', '.vob')' formatlarni qabul qilinadi.")
        return value


class PubgAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PubgAccount
        fields = '__all__'

    def to_representation(self, instance):
        account = super().to_representation(instance)
        user_id = account.get('user_fk')
        category_id = account.get('category_fk')
        medies_id = account.get('id')
        if user_id:
            user = CustomUser.objects.get(id=user_id)
            user_serializer = CustomUserSerializer(user)
            account['user'] = user_serializer.data
        if category_id:
            category = Category.objects.get(id=category_id)
            category_serializer = AddCategorySerializer(category)
            account['category'] = category_serializer.data
        if medies_id:
            medies = PubgAccountMedia.objects.filter(account_fk=medies_id).all()
            user_serializer = PubgAccountAddMediaSerializer(medies, many=True)
            account['medies'] = user_serializer.data
        return account
