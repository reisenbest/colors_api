from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from .serializers import *

palette_tag = 'Палитры'
color_tag = 'Цвета'

get_palette_list_scheme = extend_schema(
    description="Получение списка палитр текущего пользователя.",
    summary="Получение списка палитр текущего пользователя.",
    tags=[palette_tag, ],
    responses={200: PaletteOutputSerializer(many=True)},
)

create_palette_scheme = extend_schema(
    description="Создание новой палитры для текущего пользователя.",
    summary="Создание новой палитры для текущего пользователя.",
    request=PaletteInputSerializer,
    tags=[palette_tag, ],
    responses={
        201: OpenApiResponse(description="Успешное создание палитры"),
        400: OpenApiResponse(description="Ошибка валидации данных или ошибка при создании палитры ")
    },
)

get_palette_by_title_scheme = extend_schema(
    description="Получение палитры текущего пользовтеля по названию палитры",
    summary="Получение палитры текущего пользовтеля по названию палитры",
    parameters=[
        OpenApiParameter(
            name='palette_title',
            type=str,
            location=OpenApiParameter.PATH,
            description='Название палитры которую надо получить',
            required=True,
        )
    ],
    tags=[palette_tag, ],
    responses={
        200: OpenApiResponse(response=PaletteOutputSerializer(many=False),
                             description="Успешное получение палитры"),
        404: OpenApiResponse(description="Палитра не найдена")
    },
)

update_palette_by_title_scheme = extend_schema(
    description="Изменение палитры для текущего пользователя по названию палитры",
    summary="Изменение палитры для текущего пользователя по названию палитры",
    request=PaletteInputSerializer,
    parameters=[
        OpenApiParameter(
            name='palette_title',
            type=str,
            location=OpenApiParameter.PATH,
            description='Название палитры которую надо изменить',
            required=True,
        )
    ],
    tags=[palette_tag, ],
    responses={
        201: OpenApiResponse(response=PaletteOutputSerializer(many=False),
                             description="Успешное изменение палитры"),
        400: OpenApiResponse(description="Ошибка при создании палитры"),
        404: OpenApiResponse(description="Палитра не найдена")

    },
)

delete_palette_by_title_scheme = extend_schema(
    description="Удаление палитры для текущего пользователя по названию палитры",
    summary="Удаление палитры для текущего пользователя по названию палитры",
    parameters=[
        OpenApiParameter(
            name='palette_title',
            type=str,
            location=OpenApiParameter.PATH,
            description='Название палитры которую надо удалить',
            required=True,
        )
    ],
    tags=[palette_tag, ],
    responses={
        201: OpenApiResponse(description="Успешное удаление палитры"),
        404: OpenApiResponse(description="Палитра не найдена")
    },
)

get_colors_list_by_user_scheme = extend_schema(
    description="Получение всех цветов во всех палитрах для текущего пользователя",
    summary="Получение всех цветов во всех палитрах для текущего пользователя",
    tags=[color_tag, ],
    responses={200: OpenApiResponse(response=ColorOutputSerializer(many=True),
                                    description="Успешное получение всех цветов из всех палитр пользователя")},
)

get_colors_list_by_palette_title_scheme = extend_schema(
        description="Получение коллекции цветов по названию палитры",
        summary="Получение коллекции цветов по названию палитры",
        tags=[color_tag,],
        parameters=[
            OpenApiParameter(
                name='palette_title',
                type=str,
                location=OpenApiParameter.PATH,
                description='Название палитры цвета из которой надо получить',
                required=True,
            ),

        ],
        responses={
            200: OpenApiResponse(response=ColorOutputSerializer(many=True),
                                 description="Успешное получение цветов из конкретной палитры"),
            404: OpenApiResponse(description="Ошибка получения цветов из конкретной палитры")
        },
    )

add_color_to_palette_scheme = extend_schema(
        description="Добавление нового цвета в конкретную палитру",
        summary="Добавление нового цвета в конкретную палитру",
        request=ColorInputSerializer,
        parameters=[
            OpenApiParameter(
                name='palette_title',
                type=str,
                location=OpenApiParameter.PATH,
                description='Название палитры цвет в которую надо добавить',
                required=True,
            ),

        ],
        tags=[color_tag, ],
        responses={
            201: OpenApiResponse(description="Цвет добавлен в палитру"),
            400: OpenApiResponse(description="Ошибка при добавлении цвета в палитру ")
        },
    )

get_color_by_palette_and_hex_scheme = extend_schema(
        description="Получение цвета по названию палитры и hex цвета",
        summary="Получение цвета по названию палитры и hex цвета",
        request=ColorOutputSerializer,
        parameters=[
            OpenApiParameter(
                name='palette_title',
                type=str,
                location=OpenApiParameter.PATH,
                description='Название палитры в которой нужно искать цвет',
                required=True,
            ),
            OpenApiParameter(
                name='hex_color',
                type=str,
                location=OpenApiParameter.PATH,
                description='искомый цвет в формате hex (6 цифр) без #',
                required=True,
            )

        ],
        tags=[color_tag, ],
        responses={
            200: OpenApiResponse(ColorOutputSerializer(many=False)),
            404: OpenApiResponse(description="Цвет не найден")
        },
    )

update_color_by_palette_and_hex_scheme = extend_schema(
    description="Изменение указанного цвета в указанной палитре",
    summary="Изменение указанного цвета в указанной палитре",
    request=ColorInputSerializer,
    tags=[color_tag,],
    parameters=[
            OpenApiParameter(
                name='palette_title',
                type=str,
                location=OpenApiParameter.PATH,
                description='Название палитры в которой нужно изменить цвет',
                required=True,
            ),
            OpenApiParameter(
                name='hex_color',
                type=str,
                location=OpenApiParameter.PATH,
                description='цвет который нужно изменить в формате hex (6 цифр) без #',
                required=True,
            )

        ],
    responses={
        200: OpenApiResponse(response=ColorOutputSerializer(many=False),
                             description='Цвет успешно изменен'),
        404: OpenApiResponse(description="Цвет или палитра не найдены")
    }
)


delete_color_by_palette_and_hex_scheme = extend_schema(
    description="Удаление указанного цвета в указанной палитре",
    summary="Удаление указанного цвета в указанной палитре",
    tags=[color_tag,],
    parameters=[
            OpenApiParameter(
                name='palette_title',
                type=str,
                location=OpenApiParameter.PATH,
                description='Название палитры в которой нужно удалить цвет',
                required=True,
            ),
            OpenApiParameter(
                name='hex_color',
                type=str,
                location=OpenApiParameter.PATH,
                description='цвет который нужно удалить в формате hex (6 цифр) без #',
                required=True,
            )

        ],
    responses={
        200: OpenApiResponse(description='Цвет успешно удален'),
        404: OpenApiResponse(description="Цвет или палитра не найдены")
    }
)
