import sys
import argparse
from pathlib import Path

# Добавляем корень проекта в sys.path, чтобы импорты работали корректно

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
sys.path.append(str(project_root))

from src.photo_date_stamper import file_utils
from src.photo_date_stamper import exif_processor
from src.photo_date_stamper import image_processor


def process_folder(folder_path: Path):
    """
    Основная логика обработки папки.
    """
    if not folder_path.exists():
        print(f"❌ Ошибка: Папка {folder_path} не существует.")
        return

    # 1. Интерактивный вопрос про бэкап
    print(f"📂 Выбрана папка: {folder_path}")
    answer = input("Создать резервную копию перед обработкой? [Y/n]: ").strip().lower()

    if answer in ("", "y", "yes"):
        print("⏳ Создаю бэкап...")
        try:
            file_utils.create_backup(folder_path)
        except Exception as e:
            print(f"❌ Ошибка при создании бэкапа: {e}")
            print("Останавливаю работу во избежание потери данных.")
            return
    else:
        print("⚠ Бэкап пропущен. Изменения будут необратимы.")

    # 2. Получаем файлы
    images = file_utils.get_target_files(folder_path)
    print(f"Найдено изображений: {len(images)}")

    stats = {"processed": 0, "skipped": 0, "errors": 0}

    # 3. Обработка
    for img_path in images:
        try:
            date = exif_processor.get_exif_date(img_path)

            if date:
                image_processor.write_date_to_image(img_path, date, output_path=None)

                print(f"✅ {img_path.name}: {date.strftime('%d.%m.%Y')}")
                stats["processed"] += 1
            else:
                # Даты нет
                print(f"⏩ {img_path.name}: Нет EXIF даты -> Пропуск")
                stats["skipped"] += 1

        except Exception as e:
            print(f"❌ {img_path.name}: Ошибка обработки — {e}")
            stats["errors"] += 1

    # 4. Итоги
    print("-" * 30)
    print("🎉 Готово!")
    print(f"Обработано: {stats['processed']}")
    print(f"Пропущено:  {stats['skipped']}")
    print(f"Ошибок:     {stats['errors']}")


def main():
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description="Автоматическое добавление даты на фото.")
    parser.add_argument("folder", type=str, help="Путь к папке с фотографиями")

    args = parser.parse_args()

    folder = Path(args.folder)
    process_folder(folder)


if __name__ == "__main__":
    main()