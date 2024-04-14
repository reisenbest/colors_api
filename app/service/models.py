from django.db import models
from .validators import ColorHexValidator
from .utils import autocomplete_title_field
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError

UserModel = get_user_model()

class Palette(models.Model):
    user = models.ForeignKey(UserModel, related_name='user', on_delete=models.CASCADE)
    title = models.CharField(('Название'), max_length=50, blank=False)
    

    class Meta:
        verbose_name = 'Палитры'
        verbose_name_plural = 'Палитры'

        constraints = [
            UniqueConstraint(fields=['user', 'title'],
                             name='unique_palette_with_user',
                             violation_error_message='У этого пользователя уже есть палитра с таким названием'
                             )
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    def __str__(self):
        return f'ID: {self.id}, {self.title}'
    
class Color(models.Model):
    palette = models.ForeignKey(Palette, on_delete=models.CASCADE,
                                verbose_name='Идентификатор палитры',
                                )
    hex_color = models.CharField(('HEX цвета'),
                           max_length=7,
                           blank=False,
                           validators=[ColorHexValidator()],
                           )
    title = models.CharField(('Название'), 
                             max_length=50,
                             blank=True,
                             help_text='Оставьте пустым и название будет сгенерировано автоматически')




    class Meta:
        verbose_name = 'Цвета'
        verbose_name_plural = 'Цвета'
        constraints = [
            UniqueConstraint(fields=['palette', 'hex_color', ], name='unique_palette_with_hex_color',
                             violation_error_message='В одной палитре не может быть двух одинаковых цветов'),
            UniqueConstraint(fields=['palette', 'title', ], name='unique_palette_with_title',
                             violation_error_message='В одной палитре не может быть двух одинаковых цветов'),
        ]

    def save(self, *args, **kwargs):
            self.hex_color = self.hex_color.lower()
            if not self.title:
                title = autocomplete_title_field(self.hex_color)
                self.title = title
            super().save(*args, **kwargs)

        
    def __str__(self):
        return f'ID: {self.id}, {self.title}'
