from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from .views import PaletteAdminAPIViewset, ColorAdminAPIViewset, UserAdminAPIViewset


palette_router = DefaultRouter()
palette_router.register('adminpalette', PaletteAdminAPIViewset, basename='admin')

color_router = DefaultRouter()
color_router.register('admincolor', ColorAdminAPIViewset, basename='admin')

user_router = DefaultRouter()
user_router.register('adminuser', UserAdminAPIViewset, basename='admin')


urlpatterns = [
    path('', include(palette_router.urls)),
    path('', include(color_router.urls)),
    path('', include(user_router.urls)),
]


