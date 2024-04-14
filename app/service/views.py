from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .docs import *
from .queries import PaletteQueries, ColorQueries
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication, JWTAuthentication


class PaletteListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    output_serializer = PaletteOutputSerializer
    input_serializer = PaletteInputSerializer

    @get_palette_list_scheme
    def get(self, request):
        queryset = Palette.objects.filter(user=request.user).select_related('user')
        data = self.output_serializer(queryset, many=True).data
        return Response(data)


    @create_palette_scheme
    def post(self, request):
        serializer = self.input_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data['title']
        try:
            Palette.objects.create(title=title, user=request.user)
            return Response({"detail": f"Палитра с названием - {title} успешно создана."},
                            status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"detail": f"Ошибка при создании палитры: палитра с таким названием уже существует"},
                            status=status.HTTP_400_BAD_REQUEST)


class PaletteGetDetailUpdateDeleteAPIView(APIView):
    '''
        сделал через тайтл так как только он уникален у каждого пользователя,
        а по id искать - плохая идея, так как они сквозные для всех пользователей
        и привязанных к ним палитр
    '''

    output_serializer = PaletteOutputSerializer
    input_serializer = PaletteInputSerializer

    @get_palette_by_title_scheme
    def get(self, request, palette_title):
        try:
            palette_instance = PaletteQueries.get_palette_by_title_and_user(palette_title, request)

        except ObjectDoesNotExist:
            return Response({"detail": f"Палитра с названием - {palette_title} не найдена"},
                            status=status.HTTP_404_NOT_FOUND)

        data = self.output_serializer(palette_instance).data
        return Response(data, status=status.HTTP_200_OK)

    @update_palette_by_title_scheme
    def put(self, request, palette_title):
        try:
            palette_instance = PaletteQueries.get_palette_by_title_and_user(palette_title, request)
        except ObjectDoesNotExist:
            return Response({"detail": f"Палитра с названием - {palette_title} не найдена"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.input_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        palette_instance.title = serializer.validated_data.get('title')
        try:
            palette_instance.full_clean()
            palette_instance.save()
        except ValidationError as error:
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)

        data_for_response = self.output_serializer(palette_instance).data
        return Response(data_for_response, status=status.HTTP_200_OK)

    @delete_palette_by_title_scheme
    def delete(self, request, palette_title):
        try:
            palette_instance = PaletteQueries.get_palette_by_title_and_user(palette_title, request)
        except ObjectDoesNotExist:
            return Response({"detail": f"Палитра с названием - {palette_title} не найдена."},
                            status=status.HTTP_404_NOT_FOUND)

        palette_instance.delete()
        return Response({'detail': f'Палитра с названием - {palette_title} успешно удалена'},
                        status=status.HTTP_200_OK)


class ColorListAPIView(APIView):
    output_serializer = ColorOutputSerializer

    @get_colors_list_by_user_scheme
    def get(self, request):
        queryset = Color.objects.filter(palette__user=request.user).select_related('palette__user')
        data = self.output_serializer(queryset, many=True).data
        return Response(data)


class ColorByPaletteListCreateAPIView(APIView):
    output_serializer = ColorOutputSerializer
    input_serializer = ColorInputSerializer

    @get_colors_list_by_palette_title_scheme
    def get(self, request, palette_title):
        try:
            palette_instance = PaletteQueries.get_palette_by_title_and_user(palette_title, request)
        except ObjectDoesNotExist:
            return Response({"detail": f"Палитра с названием - {palette_title} не найдена"},
                            status=status.HTTP_404_NOT_FOUND)

        queryset = Color.objects.filter(palette=palette_instance).select_related('palette')
        data = self.output_serializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @add_color_to_palette_scheme
    def post(self, request, palette_title):
        serializer = self.input_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hex_color = serializer.validated_data['hex_color']

        try:
            palette_instance = PaletteQueries.get_palette_by_title_and_user(palette_title, request)
            color_instance = Color.objects.create(palette=palette_instance,
                                                  hex_color=hex_color)

            return Response({
                "detail": f"Цвет с названием {color_instance.title} и hex: {hex_color} был добавлен в палитру с именем {palette_title}"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "detail": f"Ошибка при создании добавлении цвета в палитру {palette_title}: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)


class ColorDetailUpdateDeleteAPIView(APIView):
    output_serializer = ColorOutputSerializer
    input_serializer = ColorInputSerializer

    @get_color_by_palette_and_hex_scheme
    def get(self, request, palette_title, hex_color):
        hex_color = hex_color.lower()
        try:
            color_instance = ColorQueries.get_color_by_palette_user(request, palette_title, hex_color)
        except ObjectDoesNotExist:
            return Response({'detail': f'цвет {hex_color} в палитре {palette_title} не найден'},
                            status=status.HTTP_404_NOT_FOUND)

        data = self.output_serializer(color_instance, many=False).data
        return Response(data, status=status.HTTP_200_OK)

    @update_color_by_palette_and_hex_scheme
    def put(self, request, palette_title, hex_color):
        hex_color = hex_color.lower()

        try:
            palette_instance = PaletteQueries.get_palette_by_title_and_user(palette_title, request)
        except ObjectDoesNotExist:
            return Response({'detail': f'палитра {palette_title} не найдена'}, status=status.HTTP_404_NOT_FOUND)

        try:
            color_instance = ColorQueries.get_color_by_palette_user(request, palette_title, hex_color)
        except ObjectDoesNotExist:
            return Response({'detail': f'цвет {hex_color} в палитре {palette_title} не найден'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.input_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        color_instance.hex_color = serializer.validated_data.get('hex_color', color_instance.hex_color)
        color_instance.palette = palette_instance
        color_instance.title = None

        color_instance.save()

        data_response = self.output_serializer(color_instance, many=False).data
        return Response(data_response, status=status.HTTP_200_OK)

    @delete_color_by_palette_and_hex_scheme
    def delete(self, request, palette_title, hex_color):
        hex_color = hex_color.lower()
        try:
            color_instance = ColorQueries.get_color_by_palette_user(request, palette_title, hex_color)
        except ObjectDoesNotExist:
            return Response({'detail': f'цвет #{hex_color} в палитре {palette_title} не найден'},
                            status=status.HTTP_404_NOT_FOUND)

        color_instance.delete()
        return Response({'detail': f'цвет #{hex_color} успешно удален из палитры {palette_title}'},
                        status=status.HTTP_200_OK)
