import psycopg2
import os
import logging
from pathlib import Path


class PostgresScriptRunner:
    def __init__(self, host, database, user, password, port=5432, scripts_folder='../static/db'):
        self.db_config = {
            'host': host,
            'database': database,
            'user': user,
            'password': password,
            'port': port
        }
        self.scripts_folder = scripts_folder
        self.setup_logging()
        self.logger: logging.Logger

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def execute_scripts(self, script_files, stop_on_error=True):
        """
        Выполняет SQL-скрипты в заданном порядке

        :param script_files: список путей к SQL-файлам
        :param stop_on_error: остановить выполнение при ошибке
        """
        conn = None
        try:
            conn = psycopg2.connect(**self.db_config)
            conn.autocommit = False
            cursor = conn.cursor()

            self.logger.info("Подключение к БД установлено")

            for script_file in script_files:
                script_path = Path(f'{self.scripts_folder}/{script_file}')

                if not script_path.exists():
                    self.logger.error(f"Файл не найден: {script_file}")
                    if stop_on_error:
                        raise FileNotFoundError(f"SQL файл не найден: {script_file}")
                    continue

                self.logger.info(f"Выполнение: {script_file}")

                try:
                    with open(script_path, 'r', encoding='utf-8') as f:
                        sql_content = f.read()

                    # Разделение скрипта на отдельные команды
                    commands = sql_content.split(';')

                    for command in commands:
                        command = command.strip()
                        if command and not command.startswith('--'):
                            cursor.execute(command)

                    self.logger.info(f"Успешно выполнено: {script_file}")

                except Exception as e:
                    self.logger.error(f"Ошибка в скрипте {script_file}: {str(e)}")
                    if stop_on_error:
                        conn.rollback()
                        raise
                    else:
                        conn.rollback()
                        continue

            conn.commit()
            self.logger.info("Все скрипты выполнены успешно")

        except Exception as e:
            self.logger.error(f"Ошибка выполнения: {str(e)}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                cursor.close()
                conn.close()
                self.logger.info("Соединение закрыто")


# Пример использования
if __name__ == "__main__":
    runner = PostgresScriptRunner(
        host='localhost',
        database='doc_generator_db',
        user='postgres',
        password='root',
        port=5433
    )
    # Настройки

    scripts = [
        'initial_script.sql',
        'fill_organizations_script.sql',
        'fill_workers_script.sql',
        'fill_departments_script.sql',
    ]
    # Список скриптов для выполнения

    # Запуск
    runner.execute_scripts(scripts, stop_on_error=True)