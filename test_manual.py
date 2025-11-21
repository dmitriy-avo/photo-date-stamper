from datetime import datetime
from src.photo_date_stamper.image_processor import write_date_to_image
from src.photo_date_stamper.exif_processor import get_exif_date

# 1. Указываем пути
source_file = "photo.jpg"
output_file = "photo_stamped.jpg"

# 2. Придумываем дату (например, сегодняшний день)
fake_date = get_exif_date(source_file)

print(f"Обрабатываю файл: {source_file}...")

# 3. Вызываем твою функцию
try:
    write_date_to_image(source_file, fake_date, output_file)
    print(f"Готово! Проверь файл {output_file}")
except Exception as e:
    print(f"Ошибка: {e}")