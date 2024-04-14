from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from .managers import CustomUserManager



class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
    )
    login = models.CharField(verbose_name='Логин',
                             max_length=50,
                             unique=True,
                             blank=False)


    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username}'











