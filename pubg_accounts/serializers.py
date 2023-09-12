from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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



