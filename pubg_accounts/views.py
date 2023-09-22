from asgiref.sync import async_to_sync
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
import uuid
from channels.layers import get_channel_layer

from user.views import user_chack, admin_chack
from .serializers import *
from django.core.mail import send_mail
from django.conf import settings
import random
from django.utils import timezone


class PubgAccountCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PubgAccountCreateSerializer)
    def post(self, request):
        """
        user pubg account create qilishi (adminga tekshiruvga jo'natiladi)
        """
        user_chack(request.user.role)
        serializer = PubgAccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            status_type = "tekshiruvda"
            serializer.save(user_fk=user, status_type=status_type)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PubgAccountAddMediaView(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PubgAccountAddMediaSerializer)
    def post(self, request):
        """
        user Pubg account uchun media video rasm qo'shish
        """
        user_chack(request.user.role)
        serializer = PubgAccountAddMediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PubgAccountsView(APIView):

    def get(self, request):
        """
        Pubg get "sotuvda" all accounts
        """
        accounts = PubgAccount.objects.filter(status_type='sotuvda').order_by('-id').all()
        serializer = PubgAccountsSerializer(accounts, many=True)
        return Response(serializer.data)


class PubgAccountView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('account_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True)
    ])
    def get(self, request):
        """
        Pubg get account
        """
        account_id = request.query_params.get('account_id')
        account = PubgAccount.objects.filter(id=account_id, status_type='sotuvda').first()
        if account:
            serializer = PubgAccountsSerializer(account)
            return Response(serializer.data)
        return Response({'error': 'Account topilamdi!'}, status=404)


class PubgAccountsUnderInvestigationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Admin uchun Tekshiruvga yuborilgan akkauntlar
        """
        admin_chack(request.user.role)
        accounts = PubgAccount.objects.filter(status_type="tekshiruvda").all()
        serializer = PubgAccountsSerializer(accounts, many=True)
        return Response(serializer.data)


class PubgAccountUnderInvestigationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('account_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True)
    ])
    def get(self, request):
        """
        Admin tekshiruvdagi accauntni ko'rishi
        """
        admin_chack(request.user.role)
        account_id = request.query_params.get('account_id')
        account = PubgAccount.objects.filter(id=account_id, status_type='tekshiruvda').first()
        if account:
            serializer = PubgAccountsSerializer(account)
            return Response(serializer.data)
        return Response({'error': 'Account topilamdi!'}, status=404)


class AdminPubgAccountUnderInvestigationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('account_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
        openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True, description="'sotuvda' yoki 'bekor_qilindi'"),
    ])
    def put(self, request):
        """
        Admin uchun Tekshiruvga yuborilgan akkauntni bekor qilishi yoki sotuvga qo'yishi
        status = ("sotuvda", "bekor_qilindi")
        """
        admin_chack(request.user.role)
        account_id = request.query_params.get('account_id')
        status = request.query_params.get('status')
        try:
            account = PubgAccount.objects.get(id=account_id)
        except PubgAccount.DoesNotExist:
            return Response({'detail': "Account not found!"}, status=404)
        if status not in ["sotuvda", "bekor_qilindi"]:
            return Response({'detail': 'status faqat ["sotuvda", "bekor_qilindi"] qiymatlarni qabul qiladi!'}, status=422)
        if account.status_type == status:
            return Response({'detail': 'Account oldin shunday ham shu statusda!'}, status=401)
        if status == status == "bekor_qilindi":
            medies = PubgAccountMedia.objects.filter(account_fk=account.id).all()
            if medies.exists():
                [media.delete() for media in medies]
        account.status_type = status
        account.save()
        return Response({'detail': 'Success'}, status=200)


class UserOrderPostView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=UserOrderPostSerializer)
    def post(self, request):
        """
        User Account uchun buyurtma berishi
        """
        user_chack(request.user.role)
        serializer = UserOrderPostSerializer(data=request.data)
        if serializer.is_valid():
            account_id = serializer.validated_data['account_fk'].id
            account = PubgAccount.objects.filter(id=account_id, status_type="sotuvda")
            if account.exists():
                serializer.save(user_fk=request.user, order_status="jarayonda")
                return Response(serializer.data, status=201)
            else:
                return Response({'detail': 'Sotuvda bo\'lmagan account!'}, status=400)
        return Response(serializer.errors, status=400)


class UserAllOrdersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True,
                          description='"jarayonda", "tugallandi" "bekor_qilindi"'),
    ])
    def get(self, request):
        """
        User PubgAccount uchun hamma buyurtmalarini ko'rishi
        """
        user_chack(request.user.role)
        order_status = request.query_params.get('status')
        if order_status not in ["jarayonda", "tugallandi", "bekor_qilindi"]:
            return Response({"detail": 'Status faqat ["jarayonda", "tugallandi" "bekor_qilindi"] bo\'lishi mumkin!'}, status=422)
        orders = PubgAccountOrder.objects.filter(user_fk=request.user.id, order_status=order_status).order_by('-id').all()
        serializer = PubgOrdersSerializer(orders, many=True)
        return Response(serializer.data, status=200)


class AdminOrderCompletedPubgAccountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('order_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
        openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True, description="'bekor_qilindi' yoki 'tugallandi'"),
        openapi.Parameter('sold_price', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False),
        openapi.Parameter('price_paid_to_us', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False),
    ])
    def put(self, request):
        """
        Admin uchun accaunt sotilgandan so'ng yoki sotilmasa usha buyurtmani yakunlash,
        Agar account sotilsa avtomaticheski account sotuvdan olib tashlanadi va buyurtma istoriyasiga qo'shiladi
        status faqat "bekor_qilindi", "tugallandi" bo'lishi mumkin
        """
        admin_chack(request.user.role)
        order_id = request.query_params.get('order_id')
        status = request.query_params.get('status')
        sold_price = request.query_params.get('sold_price')
        price_paid_to_us = request.query_params.get('price_paid_to_us')
        try:
            order = PubgAccountOrder.objects.get(id=order_id)
        except PubgAccountOrder.DoesNotExist:
            return Response({'detail': "Order not found!"}, status=404)
        if order.order_status == "tugallandi":
            return Response({'detail': 'Buyurtma allaqachon tugallangan!'}, status=401)
        elif order.order_status == "bekor_qilindi":
            return Response({'detail': 'Buyurtma allaqachon bekor qilingan!'}, status=402)
        if status == "bekor_qilindi":
            order.order_status = "bekor_qilindi"
            order.save()
            return Response({'detail': 'Buyurtma bekor qilindi!'}, status=400)
        elif status == "tugallandi":
            if sold_price is None or price_paid_to_us is None:
                return Response({'detail': 'status "tugallandi" uchun price_paid_to_us va sold_price kirilishi shart!'}, status=422)
            order.order_status = "tugallandi"
            PubgAccountHistory.objects.create(
                account_fk=order.account_fk,
                user_fk=order.user_fk,
                sold_price=sold_price,
                price_paid_to_us=price_paid_to_us
            )
            account = PubgAccount.objects.filter(id=order.account_fk.id).first()
            account.status_type = "sotildi"
            medies = PubgAccountMedia.objects.filter(account_fk=account.id).all()
            if medies.exists():
                [media.delete() for media in medies]
            order.save()
            account.save()
            return Response({'detail': 'Buyurtma tugallandi!'}, status=200)
        else:
            return Response({'detail': 'Status faqat ["bekor_qilindi", "tugallandi"] bo\'lishi mumkin!'}, status=422)


class AdminAllOrdersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True,
                          description='"jarayonda", "tugallandi" "bekor_qilindi"'),
    ])
    def get(self, request):
        """
        Admin PubgAccount uchun hamma buyurtmalarini ko'rishi
        """
        admin_chack(request.user.role)
        order_status = request.query_params.get('status')
        if order_status not in ["jarayonda", "tugallandi", "bekor_qilindi"]:
            return Response({"detail": 'Status faqat ["jarayonda", "tugallandi" "bekor_qilindi"] bo\'lishi mumkin!'}, status=422)
        orders = PubgAccountOrder.objects.filter(order_status=order_status).order_by('-id').all()
        serializer = PubgOrdersSerializer(orders, many=True)
        return Response(serializer.data, status=200)