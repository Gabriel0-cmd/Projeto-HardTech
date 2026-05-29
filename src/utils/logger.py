"""Sistema de logging para HardTech."""

import logging
import sys
from pathlib import Path
from src.config import LOGGING_CONFIG, LOGS_DIR


def setup_logger(name: str) -> logging.Logger:
    """
    Configura e retorna um logger.

    Args:
        name: Nome do logger (geralmente __name__)

    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)

    # Não adicionar handlers se já existirem
    if logger.handlers:
        return logger

    logger.setLevel(LOGGING_CONFIG["level"])

    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOGGING_CONFIG["level"])

    # Handler para arquivo
    log_file = LOGS_DIR / "hardtech.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(LOGGING_CONFIG["level"])

    # Formato
    formatter = logging.Formatter(LOGGING_CONFIG["format"])
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
