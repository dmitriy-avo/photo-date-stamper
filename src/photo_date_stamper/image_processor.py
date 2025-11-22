from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from pathlib import Path


def write_date_to_image(
        source_path: str | Path,
        date: datetime,
        output_path: str | Path | None = None,
) -> None:
    """
    Записывает полупрозрачную дату на фото.
    Сохраняет высокое качество изображения.
    """
    source_path = Path(source_path)
    output_path = Path(output_path) if output_path is not None else source_path

    # 1. Открываем и сразу конвертируем в RGBA (для работы с прозрачностью)
    with Image.open(source_path) as img:
        base_image = img.convert("RGBA")

        # Создаем отдельный прозрачный слой такого же размера
        # (255, 255, 255, 0) -> полностью прозрачный фон
        txt_layer = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        # --- Настройки текста ---
        text = date.strftime("%d.%m.%Y")
        font_size = max(20, int(base_image.height / 30))

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except OSError:
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", font_size)
            except OSError:
                font = ImageFont.load_default()

        # --- Расчет координат ---
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        padding_x = max(20, int(base_image.width * 0.03))
        padding_y = max(20, int(base_image.height * 0.03))

        x = base_image.width - text_width - padding_x
        y = base_image.height - text_height - padding_y
        y -= int(font_size * 0.15)

        # --- Цвета с прозрачностью (Alpha) ---
        # Четвертое число (0-255) — это непрозрачность.
        # 180 — это примерно 70% видимости (легкая прозрачность)
        # 128 — это 50% видимости
        opacity = 128
        text_color = (255, 0, 0, opacity)  # Красный полупрозрачный
        outline_color = (0, 0, 0, opacity)  # Черный полупрозрачный

        # --- Рисование на прозрачном слое ---
        thickness = 2
        for adj_x in range(-thickness, thickness + 1):
            for adj_y in range(-thickness, thickness + 1):
                if adj_x != 0 or adj_y != 0:
                    draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline_color)

        draw.text((x, y), text, font=font, fill=text_color)

        # --- Слияние слоев ---
        # alpha_composite накладывает txt_layer поверх base_image, учитывая прозрачность
        combined = Image.alpha_composite(base_image, txt_layer)

        # --- Конвертация обратно в RGB (JPEG не умеет RGBA) ---
        final_img = combined.convert("RGB")

        # --- Сохранение с высоким качеством ---
        exif_bytes = img.info.get('exif')

        save_kwargs = {
            "quality": 95,  # Высокое качество (стандарт ~75)
            "subsampling": 0  # Сохраняем четкость цветов (4:4:4)
        }

        if exif_bytes:
            save_kwargs["exif"] = exif_bytes

        final_img.save(output_path, **save_kwargs)

