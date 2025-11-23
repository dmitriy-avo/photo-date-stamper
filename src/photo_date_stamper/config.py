from typing import Tuple


class Config:
    # --- Настройки Шрифта ---
    # Имена файлов шрифтов для разных ОС
    FONT_NAME_WINDOWS = "arial.ttf"
    FONT_NAME_LINUX = "DejaVuSans.ttf"

    # Коэффициент размера шрифта.
    # Размер = Высота изображения / FONT_RATIO
    FONT_RATIO = 30

    # Минимальный размер шрифта в пикселях
    MIN_FONT_SIZE = 20

    # --- Настройки Даты ---
    DATE_FORMAT = "%d.%m.%Y"  # Например: 27.10.2023

    # --- Настройки Цвета и Прозрачности ---
    # (R, G, B, Alpha). Alpha: 0 - прозрачный, 255 - непрозрачный.
    OPACITY = 160

    # Красный цвет текста
    TEXT_COLOR: Tuple[int, int, int, int] = (255, 0, 0, OPACITY)

    # Черная обводка
    OUTLINE_COLOR: Tuple[int, int, int, int] = (0, 0, 0, OPACITY)

    # Толщина обводки
    OUTLINE_THICKNESS = 2

    # --- Настройки отступов ---
    # Отступ от края в процентах (0.03 = 3%)
    PADDING_RATIO = 0.03

    # Минимальный отступ в пикселях
    MIN_PADDING = 20

    # Настройки сохранения JPEG
    JPEG_QUALITY = 95
    JPEG_SUBSAMPLING = 0