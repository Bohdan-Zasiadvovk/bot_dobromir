import logging
import atexit
import concurrent.futures


class BackgroundLogger:
    def __init__(self, log_file_name='my_log.txt', error_log_file_name='error_log.txt'):
        # Инициализация логгера
        self.logger = logging.getLogger('my_logger')
        self.logger.setLevel(logging.DEBUG)

        # Создание форматтера для логов
        log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Создание и настройка обработчика для записи всех сообщений в файл
        log_handler = logging.FileHandler(log_file_name)
        log_handler.setLevel(logging.DEBUG)
        log_handler.setFormatter(log_format)

        # Создание и настройка обработчика для записи ошибок в отдельный файл
        error_handler = logging.FileHandler(error_log_file_name)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(log_format)

        # Добавление обработчиков к логгеру
        self.logger.addHandler(log_handler)
        self.logger.addHandler(error_handler)

        # Асинхронное логирование в фоновом потоке
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        atexit.register(self.close)

    def log(self, message):
        # Логирование сообщения в фоновом потоке
        self.executor.submit(self.logger.debug, message)

    def log_error(self, error_message):
        # Логирование ошибки в фоновом потоке
        self.executor.submit(self.logger.error, error_message)

    def close(self):
        # Завершение работы логгера
        logging.shutdown()

# Пример использования
# logger = BackgroundLogger()
#
# try:
#     # Некоторый код, который может вызвать ошибку
#     result = 1 / 0
# except Exception as e:
#     logger.log_error(f'Ошибка: {str(e)}')
#
# # Весь вывод консоли будет записан в файл
# with open('console_output.txt', 'w') as console_output_file:
#     import sys
#     sys.stdout = console_output_file
#
#     print('Привет, это вывод в консоль.')
#     print('Этот текст также будет записан в файл console_output.txt.')
#
#     # Восстановление стандартного вывода
#     sys.stdout = sys.__stdout__
#
# # Логи будут записаны в фоновом потоке перед завершением работы скрипта
