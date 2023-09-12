from asgiref.sync import async_to_sync
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser
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


def generate_verification_code():
    return str(random.randint(100000, 999999))


class CustomUserCreateView(APIView):
    @swagger_auto_schema(request_body=CustomUserSerializer)
    def post(self, request):
        """
        User create (parol 5 tadan kam emas)
        """
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            users = CustomUser.objects.all()

            password = serializer.validated_data['password']
            if len(password) < 5:
                return Response({'password': ['Parol 5 tadan kam bo\'lmasligi kerak!']},
                                status=status.HTTP_400_BAD_REQUEST)

            first_name = serializer.validated_data.get('first_name')
            if not first_name:
                return Response({'error': 'Ism kirtilmadi!'}, status=status.HTTP_400_BAD_REQUEST)

            email = serializer.validated_data.get('email')
            if not email:
                return Response({'error': 'Email kirtilmadi!'}, status=status.HTTP_400_BAD_REQUEST)
            for user in users:
                if user.email == email:
                    return Response({'error': 'Email ro\'yxatga olingan!'}, status=status.HTTP_400_BAD_REQUEST)

            phone = serializer.validated_data.get('phone')
            if not phone:
                return Response({'error': 'Phone kirtilmadi!'}, status=status.HTTP_400_BAD_REQUEST)
            for user in users:
                if user.phone == phone:
                    return Response({'error': 'Telefon raqam ro\'yxatga olingan!'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        User o'zini malumotlarini ko'rishi
        """
        if request.user:
            serialized_user = CustomUserSerializer(request.user)
            return Response(serialized_user.data)
        else:
            return Response({'error': 'You do not have permission to access this resource'},
                            status=status.HTTP_403_FORBIDDEN)


class CustomUserUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CustomUserUpdateSerializer)
    def put(self, request):
        """
        user update profile (user profildagi hohlagan malumotini o'zgartira olishi update)
        """
        user = request.user
        serializer = CustomUserUpdateSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendEmailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Emailga kod yuborish
        """
        subject = 'Confirm the code!'
        from_email = settings.EMAIL_HOST_USER  # Gmail pochta
        user_email = [request.user.email]  # Foydalanuvchi emaili

        verification_code = generate_verification_code()
        message = f'Confirmation code: {verification_code}'

        try:
            send_mail(subject, message, from_email, user_email)
            request.user.verification_code = verification_code
            request.user.save()
            return Response({'detail': f'Kod {request.user.email} ga yuborildi!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Xatolik yuz berdi: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChackEmailCodeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, verify_code):
        """
        Email kodeni tekshirish
        """
        if request.user.verification_code != 0:
            if request.user.verification_code == verify_code:
                return Response({'detail': "To'gri kod yuborildi!"}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': "Noto'gri kod yuborildi!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'detail': "Kod topilmadi!"}, status=status.HTTP_404_NOT_FOUND)


class UserUpdatePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, new_pass):
        """
        User email kod tekshiruvdan o'tgandan so'ng parolni yangilashi
        """
        if len(new_pass) < 5:
            return Response({'password': 'Parol 5 tadan kam bo\'lmasligi kerak!'},
                            status=status.HTTP_400_BAD_REQUEST)
        hashed_password = make_password(new_pass)
        request.user.password = hashed_password
        request.user.verification_code = 0
        request.user.save()

        return Response({'detail': 'Parol yangilandi.'}, status=status.HTTP_200_OK)


class AllUsersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Admin hamma userlarni ko'ra olishi
        """
        if request.user and request.user.role == "admin":
            users = CustomUser.objects.filter(role='user').order_by('-id').all()
            serializer = AllUsersSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'Faqat Admin uchun ruxsat berilgan!'}, status=status.HTTP_403_FORBIDDEN)


class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        """
        Admin user malumotlarini ko'ra olishi
        """
        if request.user and request.user.role == "admin":
            user = CustomUser.objects.filter(id=user_id, role='user').first()
            if user:
                serializer = CustomUserSerializer(user)
                return Response(serializer.data)
            else:
                return Response({'error': 'User topilmadi!'}, status=404)
        else:
            return Response({'error': 'Faqat Admin uchun ruxsat berilgan!'}, status=status.HTTP_403_FORBIDDEN)


class SupportPostView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=SupportPostSerializer)
    def post(self, request):
        """
        user Support yuborish
        """
        serializer = SupportPostSerializer(data=request.data)
        if serializer.is_valid():
            user_fk = request.user
            serializer.save(user_fk=user_fk, sanded_at=timezone.now())
            return Response({'detail': 'Yuborildi!.'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Xatolik!'}, status=status.HTTP_400_BAD_REQUEST)


class AllSupportsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, status):
        """
        Admin hamma supportlarni ko'ra olishi
        """
        if request.user and request.user.role == "admin":
            supports = Support.objects.order_by('-id').all()
            if status == 'True':
                supports = supports.filter(read=True)
            elif status == 'False':
                supports = supports.filter(read=False)
            else:
                return Response({'error': "Faqat 'True' yoki 'False' status bo'lishi kerak!"}, status=422)
            serializer = AllSupportsSerializer(supports, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'Faqat Admin uchun ruxsat berilgan!'}, status=status.HTTP_403_FORBIDDEN)


class SupportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, support_id):
        """
        Admin supportni ko'ra olishi
        """
        if request.user and request.user.role == "admin":
            support = Support.objects.filter(id=support_id).first()
            if support:
                serializer = AllSupportsSerializer(support)
                return Response(serializer.data, status=200)
            else:
                return Response({'error': "Support topilmadi!"}, status=404)
        else:
            return Response({'error': 'Faqat Admin uchun ruxsat berilgan!'}, status=status.HTTP_403_FORBIDDEN)


class ReadSupportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, support_id):
        """
        Admin supportni o'qildi qilishi
        """
        if request.user and request.user.role == "admin":
            support = Support.objects.filter(id=support_id).first()
            if support:
                if support.read != True:
                    support.read = True
                    support.save()
                    serializer = AllSupportsSerializer(support)
                    return Response(serializer.data)
                else:
                    return Response({'error': "Allaqachon o'qilgan support!"}, status=400)
            else:
                return Response({'error': 'Support topilmadi!'}, status=404)
        else:
            return Response({'error': 'Faqat Admin uchun ruxsat berilgan!'}, status=403)


class AddCategoryView(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AddCategorySerializer)
    def post(self, request):
        """
        Admin Category qo'shishi
        """
        if request.user and request.user.role == "admin":
            serializer = AddCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Faqat Admin uchun ruxsat berilgan!'}, status=403)


class CategoryUpdateView(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=UpdateCategorySerializer)
    def put(self, request, category_id):
        """
        Admin Category update
        """
        if request.user and request.user.role == "admin":
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = UpdateCategorySerializer(data=request.data, partial=True)
            if serializer.is_valid():
                if 'name' in request.data:
                    category.name = serializer.validated_data['name']
                if 'rasm' in request.data:
                    category.rasm = serializer.validated_data['rasm']
                category.save()
                response_category = UpdateCategorySerializer(category)
                return Response(response_category.data, status=200)
        else:
            return Response({'error': 'Faqat Admin uchun ruxsat berilgan!'}, status=403)


class AllCategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Umumiy hamma Categoriyalarni ko'rish
        """
        categories = Category.objects.all()
        serializer = AddCategorySerializer(categories, many=True)
        return Response(serializer.data, status=200)







