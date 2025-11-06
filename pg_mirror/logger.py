"""Logger configuration for pg-mirror"""
import sys
import logging


def setup_logger(verbose=False):
    """
    Configura o logger da aplicação
    
    Args:
        verbose: Se True, mostra mensagens DEBUG
    """
    logger = logging.getLogger('pg-mirror')
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # Remove handlers existentes
    logger.handlers = []
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # Formato detalhado
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    return logger
