from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from pathlib import Path
from .config import Config


def write_date_to_image(
        source_path: str | Path,
        date: datetime,
        output_path: str | Path | None = None,
) -> None:
    """
    Записывает полупрозрачную дату на фото, используя настройки из Config.
    """
    source_path = Path(source_path)
    output_path = Path(output_path) if output_path is not None else source_path

    with Image.open(source_path) as img:
        base_image = img.convert("RGBA")
        txt_layer = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        # 1. Форматирование даты (из конфига)
        text = date.strftime(Config.DATE_FORMAT)

        # 2. Расчет размера шрифта (из конфига)
        font_size = max(Config.MIN_FONT_SIZE, int(base_image.height / Config.FONT_RATIO))

        try:
            font = ImageFont.truetype(Config.FONT_NAME_WINDOWS, font_size)
        except OSError:
            try:
                font = ImageFont.truetype(Config.FONT_NAME_LINUX, font_size)
            except OSError:
                font = ImageFont.load_default()

        # 3. Расчет координат
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Отступы (из конфига)
        padding_x = max(Config.MIN_PADDING, int(base_image.width * Config.PADDING_RATIO))
        padding_y = max(Config.MIN_PADDING, int(base_image.height * Config.PADDING_RATIO))

        x = base_image.width - text_width - padding_x
        y = base_image.height - text_height - padding_y
        y -= int(font_size * 0.15)

        # 4. Рисование (цвета из конфига)
        thickness = Config.OUTLINE_THICKNESS
        for adj_x in range(-thickness, thickness + 1):
            for adj_y in range(-thickness, thickness + 1):
                if adj_x != 0 or adj_y != 0:
                    draw.text((x + adj_x, y + adj_y), text, font=font, fill=Config.OUTLINE_COLOR)

        draw.text((x, y), text, font=font, fill=Config.TEXT_COLOR)

        # Слияние и сохранение
        combined = Image.alpha_composite(base_image, txt_layer)
        final_img = combined.convert("RGB")

        exif_bytes = img.info.get('exif')

        save_kwargs = {
            "quality": Config.JPEG_QUALITY,
            "subsampling": Config.JPEG_SUBSAMPLING
        }

        if exif_bytes:
            save_kwargs["exif"] = exif_bytes

        final_img.save(output_path, **save_kwargs)