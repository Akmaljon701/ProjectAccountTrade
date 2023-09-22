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
            user = CustomUser.objects.filter(id=user_id).first()
            user_serializer = CustomUserSerializer(user)
            account['user'] = user_serializer.data
        if category_id:
            category = Category.objects.filter(id=category_id).first()
            category_serializer = AddCategorySerializer(category)
            account['category'] = category_serializer.data
        if medies_id:
            medies = PubgAccountMedia.objects.filter(account_fk=medies_id).all()
            user_serializer = PubgAccountAddMediaSerializer(medies, many=True)
            account['medies'] = user_serializer.data
        return account


class UserOrderPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PubgAccountOrder
        fields = '__all__'
        extra_kwargs = {
            'date': {'read_only': True},
            'user_fk': {'read_only': True},
            'order_status': {'read_only': True},
        }


class PubgAccountGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PubgAccount
        fields = ('type', 'price', 'level', 'rp', 'clothes', 'skins', 'titles', 'detail')


class PubgOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PubgAccountOrder
        fields = '__all__'

    def to_representation(self, instance):
        order = super().to_representation(instance)
        account_id = order.get('account_fk')
        user_id = order.get('user_fk')
        if account_id:
            account = PubgAccount.objects.filter(id=account_id).first()
            account_serializer = PubgAccountGetSerializer(account)
            order['account'] = account_serializer.data
        if user_id:
            user = CustomUser.objects.filter(id=user_id).first()
            user_serializer = CustomUserSerializer(user)
            order['user'] = user_serializer.data
        return order
