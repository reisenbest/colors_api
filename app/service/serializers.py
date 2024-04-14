from rest_framework import serializers
from .validators import ColorHexValidator
from .models import Color, Palette


class PaletteOutputSerializer(serializers.ModelSerializer):
    palette_id = serializers.CharField(source='pk')
    user = serializers.CharField(source='user.username')
    title = serializers.CharField(label='name')

    class Meta:
        model = Palette
        fields = ('palette_id', 'user', 'title')


class PaletteInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Palette
        fields = ('title',)


class ColorOutputSerializer(serializers.Serializer):
    color_id = serializers.CharField(source='pk')
    user = serializers.CharField(source='palette.user')
    palette = serializers.CharField(source='palette.title')
    title = serializers.CharField(label='name')
    hex_color = serializers.CharField()


class ColorInputSerializer(serializers.Serializer):
    hex_color = serializers.CharField(validators=[ColorHexValidator()])
    #palette = serializers.CharField(required=False)


    

