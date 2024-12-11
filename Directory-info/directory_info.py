import os
import logging
from collections import namedtuple
from datetime import datetime
import stat
import pwd

# Определяем namedtuple для хранения информации о файлах и директориях
FileInfo = namedtuple('FileInfo', ['name', 'extension', 'is_directory', 'parent_directory'])

# Настраиваем логирование
logging.basicConfig(
    filename='./log/directory_info.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_file_info(path):
    try:
        stats = os.stat(path)
        size = stats.st_size
        creation_time = datetime.fromtimestamp(stats.st_ctime)
        modification_time = datetime.fromtimestamp(stats.st_mtime)
        owner = pwd.getpwuid(stats.st_uid).pw_name
        
        if os.path.isdir(path):
            logging.info(f'Директория: {path}, Размер: {size} байт, Создано: {creation_time}, '
                         f'Последнее изменение: {modification_time}, Владелец: {owner}')
        else:
            logging.info(f'Файл: {path}, Размер: {size} байт, Создано: {creation_time}, '
                         f'Последнее изменение: {modification_time}, Владелец: {owner}')
    except Exception as e:
        logging.error(f'Ошибка при получении информации о {path}: {e}')

def collect_directory_info(directory_path):
    if not os.path.isdir(directory_path):
        logging.error(f'Указанный путь не является директориями: {directory_path}')
        return []

    file_info_list = []
    for root, dirs, files in os.walk(directory_path):
        parent_directory = os.path.basename(root)

        log_file_info(root)

        for file in files:
            file_path = os.path.join(root, file)
            name, extension = os.path.splitext(file)
            extension = extension[1:] 
            is_directory = False

            file_info = FileInfo(name=name, extension=extension, 
                                 is_directory=is_directory, 
                                 parent_directory=parent_directory)

            file_info_list.append(file_info)
            log_file_info(file_path)

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            name = dir
            extension = ''
            is_directory = True

            dir_info = FileInfo(name=name, extension=extension,
                                is_directory=is_directory, 
                                parent_directory=parent_directory)

            file_info_list.append(dir_info)
            log_file_info(dir_path)

    return file_info_list

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("Использование: python script.py <путь_до_директории>")
        sys.exit(1)

    directory_path = sys.argv[1]
    collect_directory_info(directory_path)
