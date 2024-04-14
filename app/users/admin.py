from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserModel
    list_display = ('username', 'login', 'is_staff', 'is_active',)
    list_filter = ('username', 'login', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'login', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'login', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'login',)
    ordering = ('username', 'login',)


admin.site.register(UserModel, CustomUserAdmin)