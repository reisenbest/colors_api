from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny


UserModel = get_user_model()



class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    @extend_schema(
        description="Аутентификация пользователя и получение токенов доступа.",
        summary="Авторизация пользователя и получение токенов для доступа",
        request=LoginSerializer,
        tags=['Регистрация, вход'],
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterUserAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        description="Регистрация нового пользователя",
        summary="Регистрация пользователя",
        request=RegisterSerializer,
        tags=['Регистрация, вход'],
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Пользователь успешно зарегистрирован."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






