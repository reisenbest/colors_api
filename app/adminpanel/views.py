
from django.shortcuts import render
from service.models import Color, Palette
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import PaletteAdminSerializer, ColorAdminSerializer, UserAdminSerializer
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema


UserModel = get_user_model()



@extend_schema(summary='Админ-панель для манипуляций с палитрами',
               tags=['Админ-палитры'])
class PaletteAdminAPIViewset(ModelViewSet):
    queryset = Palette.objects.all().select_related('user')
    serializer_class = PaletteAdminSerializer
    lookup_field = 'pk'


@extend_schema(summary='Админ-панель для манипуляций с цветами',
               tags=['Админ-цвета'])
class ColorAdminAPIViewset(ModelViewSet):
    queryset = Color.objects.all().select_related('palette__user')
    serializer_class = ColorAdminSerializer
    lookup_field = 'pk'


@extend_schema(summary='Админ-панель для манипуляций с юзерами',
               tags=['Админ-юзеры'])
class UserAdminAPIViewset(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserAdminSerializer
    lookup_field = 'pk'


