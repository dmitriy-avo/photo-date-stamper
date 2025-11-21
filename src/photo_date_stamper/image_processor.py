from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from pathlib import Path


def write_date_to_image(
        source_path: str | Path,
        date: datetime,
        output_path: str | Path | None = None,
) -> None:
    """
    Записывает дату съёмки прямо на фотографию в правый нижний угол.

    Args:
        source_path: путь к исходному изображению
        date: объект datetime — дата, которую нужно нанести
        output_path: куда сохранить результат.
                     Если None — перезапишет исходный файл
    """
    source_path = Path(source_path)
    output_path = Path(output_path) if output_path is not None else source_path

    # Открываем изображение
    with Image.open(source_path) as img:
        # Конвертируем в RGB, если вдруг PNG с прозрачностью или CMYK
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        draw = ImageDraw.Draw(img)

        # Формируем красивую строку даты
        text = date.strftime("%d.%m.%Y")

        # Динамический размер шрифта — примерно 1/30 от высоты фото
        font_size = max(20, int(img.height / 30))
        font = ImageFont.truetype("arial.ttf", font_size)


        # Получаем габариты текста
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Отступы от края — 3% от размеров, но не менее 20 px
        padding_x = max(20, int(img.width * 0.03))
        padding_y = max(20, int(img.height * 0.03))

        # Координаты правого нижнего угла
        x = img.width - text_width - padding_x
        y = img.height - text_height - padding_y

        # Немного поднимаем текст, чтобы он не касался самого края
        y -= int(font_size * 0.15)

        # # Рисуем чёрную обводку (чтобы текст читался и на светлом, и на тёмном фоне)
        # outline_range = 3
        # for adj_x in range(-outline_range, outline_range + 1):
        #     for adj_y in range(-outline_range, outline_range + 1):
        #         if adj_x != 0 or adj_y != 0:
        #             draw.text((x + adj_x, y + adj_y), text, font=font, fill="black")

        # Основной красный текст
        draw.text((x, y), text, font=font, fill="red")

        # Сохраняем с сохранением EXIF
        exif_data = img.getexif()
        if exif_data is not None:
            img.save(output_path, exif=img.info.get('exif'))
        else:
            img.save(output_path)