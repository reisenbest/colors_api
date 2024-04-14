from django.urls import path
from .views import *



urlpatterns = [
    path('palette-list/', PaletteListCreateAPIView.as_view(), name='palette-list'),
    path('palette/<str:palette_title>/', PaletteGetDetailUpdateDeleteAPIView.as_view(), 
         name='palette-detail'),

    path('colors/', ColorListAPIView.as_view(), name='color-list'),
    path('colors/<str:palette_title>/', ColorByPaletteListCreateAPIView.as_view(), name='color-list-by-palette'),

    path('colors/<str:palette_title>/<str:hex_color>/', ColorDetailUpdateDeleteAPIView.as_view(), name='color-detail'),



]
