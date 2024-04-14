

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


UserModel = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserModel
        fields = ('username', 'login',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ('username', 'login',)
