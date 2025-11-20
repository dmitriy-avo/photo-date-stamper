import shutil
from pathlib import Path
from typing import List


def get_target_files(path: str | Path | None) -> List[Path]:
    """
    Находит все изображения в указанной папке (без рекурсии).
    Игнорирует папку backup, если она есть.
    Расширения: .jpg, .jpeg, .png (регистронезависимо).

    Raises:
        FileNotFoundError: если папка не существует
        NotADirectoryError: если путь указывает на файл, а не на папку
    """


    folder = folder = Path.cwd() if path is None else Path(path)
    if not folder.exists():
        raise FileNotFoundError(f"Папка не найдена: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Указанный путь не является файлом, а не папкой: {folder}")

    image_extensions = {".jpg", ".jpeg", ".png"}

    files = []
    for file in folder.iterdir():
        if not file.is_file():
            continue
        if file.is_file() and file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            files.append(file)

    return [
        item
        for item in folder.iterdir()
        if item.is_file() and item.suffix.lower() in image_extensions
    ]


def create_backup(path: str | Path | None) -> None:
    """
        Создаёт резервную копию всех изображений из указанной папки.
        Копии помещаются в подпапку 'backup' рядом с исходной папкой.

        Поведение:
            - Если папка 'backup' уже существует — просто использует её (не очищает!).
            - Если изображение с таким именем уже есть в backup — перезаписывает его.
            - При повторных запусках копирует только те файлы, которые есть в основной папке.

        Args:
            path: путь к папке с фотографиями (строка, Path или None → текущая директория)

        Returns:
            None

        Пример:
            create_backup("/home/user/Фото")  # создаст /home/user/Фото/backup/
        """
    folder = Path.cwd() if path is None else Path(path)

    # Создаём папку backup, если её нет. exist_ok=True — не падаем, если уже есть
    backup_dir = folder / "backup"
    backup_dir.mkdir(exist_ok=True)

    all_images = get_target_files(folder)
    for image in all_images:
        destination = backup_dir / image.name
        shutil.copy2(image, destination)
