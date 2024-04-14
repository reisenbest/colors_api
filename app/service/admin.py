from django.contrib import admin
from .models import Palette, Color
# Register your models here.

@admin.register(Palette)
class PalleteAdmin(admin.ModelAdmin):
    pass

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass

