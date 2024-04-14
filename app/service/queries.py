from .models import Color, Palette

class PaletteQueries:

    @staticmethod
    def get_palette_by_title_and_user(palette_title, request):
        return Palette.objects.select_related('user').get(title=palette_title, user=request.user)


class ColorQueries:
    @staticmethod
    def get_color_by_palette_user(request, palette_title, hex_color):
        return Color.objects.select_related('palette__user').get(
            palette__user=request.user,
            palette__title=palette_title,
            hex_color=f'#{hex_color}'
        )