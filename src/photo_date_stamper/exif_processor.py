from PIL import Image, UnidentifiedImageError
from datetime import datetime
from pathlib import Path
from typing import Optional


def get_exif_date(path: str | Path | None = None) -> Optional[datetime]:
    """
    Возвращает дату съёмки из EXIF (DateTimeOriginal → DateTimeDigitized → DateTime).
    Если даты нет или она битая — возвращает None.
    """
    if path is None:
        return None

    file_path = Path(path)

    try:
        with Image.open(file_path) as img:
            exif = img.getexif()
            if exif is None:                    # у PNG и многих скриншотов EXIF отсутствует
                return None

            # Приоритет: оригинальная дата → оцифровка → последнее изменение файла
            date_str = exif.get(36867) or exif.get(36868) or exif.get(306)

            if not date_str or not isinstance(date_str, str):
                return None

            return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")

    except (OSError, UnidentifiedImageError, ValueError, AttributeError):
        # OSError — файл не открылся или повреждён
        # UnidentifiedImageError — это не изображение
        # ValueError — кривая дата
        # AttributeError — редко, если getexif() вернул что-то странное
        return None





