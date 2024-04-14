from django.core.validators import RegexValidator
import re
from django.utils.deconstruct import deconstructible



class ColorHexValidator(RegexValidator):
    regex = '^#[a-fA-F0-9]{6}$'
    message = ("Проверьте формат ввода - начинаться должен с # + допустимые цифры (0–9) и латинские буквы (A–F) (6 букв и цифр)")
    code = "invalid value"
    inverse_match = False
    flags = 0
    
    def __call__(self, value):
        super().__call__(value)
