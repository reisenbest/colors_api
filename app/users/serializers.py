from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import authenticate

UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label='Пароль',
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label='Повторите пароль',
    )

    class Meta:
        model = UserModel
        fields = ('username', 'login', 'password', 'password2', 'is_staff')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Удаляем password2 перед созданием пользователя
        user = UserModel.objects.create_user(**validated_data)
        return user




class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=150)
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only = True,
    )

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')

        if login and password:
            user = authenticate(login=login, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('Учетная запись неактивна.')
            else:
                raise serializers.ValidationError('Неверное имя пользователя или пароль.')
        else:
            raise serializers.ValidationError('Необходимо предоставить имя пользователя и пароль.')

        attrs['user'] = user
        return attrs
