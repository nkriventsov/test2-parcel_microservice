from loguru import logger
import sys

# Настройка логирования
logger.remove()  # Удаляем стандартный обработчик
logger.add(sys.stderr, level="INFO", format="{time} {level} {message}")

# Логирование в файл
logger.add("logs/app.log", level="DEBUG", rotation="10 MB", compression="zip", format="{time} {level} {message}")

__all__ = ["logger"]
