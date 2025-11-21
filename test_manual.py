from src.photo_date_stamper.exif_processor import get_exif_date

# Замени 'photo.jpg' на имя твоего файла
test_file = "photo.jpg"
date = get_exif_date(test_file)

if date:
    print(f"Ура! Дата найдена: {date}")
    print(f"Тип данных: {type(date)}") # Должно быть <class 'datetime.datetime'>
else:
    print("Дата не найдена или файл без EXIF.")