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
        Pubg account uchun media video rasm qo'shish
        """
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

    def get(self, request, account_id):
        """
        Pubg get account
        """
        account = PubgAccount.objects.filter(id=account_id).first()
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
        if request.user and request.user.role == 'admin':
            accounts = PubgAccount.objects.filter(status_type="tekshiruvda").all()
            serializer = PubgAccountsSerializer(accounts, many=True)
            return Response(serializer.data)
        return Response({'error': 'Faqat Admin uchun ruxsat berilgan!'}, status=403)