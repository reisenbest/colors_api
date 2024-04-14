from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from service.models import Palette, Color
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ColorForPaletteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('hex_color', 'title')


class PaletteForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Palette
        fields = ('title',)


class PaletteAdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    palette_id = serializers.IntegerField(source='id', read_only=True)
    colors = serializers.SerializerMethodField()

    class Meta:
        model = Palette
        fields = ('palette_id', 'user', 'username', 'title', 'colors')

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_colors(self, palette_instance):
        queryset = Color.objects.filter(palette=palette_instance)
        serialized_data = ColorForPaletteSerializer(queryset, many=True).data
        return serialized_data


class ColorAdminSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(label='username', read_only=True)
    palette_title = serializers.CharField(source='palette.title', read_only=True, required=False)

    class Meta:
        model = Color
        fields = ('username', 'palette', 'palette_title', 'hex_color', 'title')

    @extend_schema_field(OpenApiTypes.STR)
    def get_username(self, color_instance):
        return color_instance.palette.user.username


class UserAdminSerializer(serializers.ModelSerializer):
    palette = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = '__all__'

    @extend_schema_field(OpenApiTypes.STR)
    def get_palette(self, user_instance):
        queryset = Palette.objects.filter(user=user_instance)
        serialized_data = PaletteForUserSerializer(queryset, many=True).data
        return serialized_data
