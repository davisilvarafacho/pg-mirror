"""
Testes para o módulo pg_mirror.logger
"""
import pytest
import logging
from pg_mirror.logger import setup_logger


class TestSetupLogger:
    """Testes para a função setup_logger"""
    
    def test_logger_creation(self):
        """Testa criação básica do logger"""
        logger = setup_logger()
        
        assert logger is not None
        assert logger.name == 'pg-mirror'
        assert isinstance(logger, logging.Logger)
    
    def test_logger_level_info_default(self):
        """Testa que nível padrão é INFO"""
        logger = setup_logger(verbose=False)
        
        assert logger.level == logging.INFO
    
    def test_logger_level_debug_verbose(self):
        """Testa que verbose=True define nível DEBUG"""
        logger = setup_logger(verbose=True)
        
        assert logger.level == logging.DEBUG
    
    def test_logger_has_handler(self):
        """Testa que logger tem pelo menos um handler"""
        logger = setup_logger()
        
        assert len(logger.handlers) > 0
    
    def test_logger_handler_is_stream(self):
        """Testa que handler é StreamHandler"""
        logger = setup_logger()
        
        assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
    
    def test_logger_formatter(self):
        """Testa que handler tem formatter configurado"""
        logger = setup_logger()
        
        handler = logger.handlers[0]
        assert handler.formatter is not None
        
        # Testa formato da mensagem
        format_str = handler.formatter._fmt
        assert 'asctime' in format_str
        assert 'levelname' in format_str
        assert 'message' in format_str
    
    def test_logger_removes_existing_handlers(self):
        """Testa que handlers existentes são removidos"""
        # Cria logger com handler
        logger1 = setup_logger()
        handlers_count_1 = len(logger1.handlers)
        
        # Recria logger
        logger2 = setup_logger()
        handlers_count_2 = len(logger2.handlers)
        
        # Deve ter mesmo número de handlers (não acumulados)
        assert handlers_count_1 == handlers_count_2
    
    def test_logger_info_message(self, caplog):
        """Testa log de mensagem INFO"""
        logger = setup_logger(verbose=False)
        
        with caplog.at_level(logging.INFO, logger='pg-mirror'):
            logger.info("Test info message")
        
        assert "Test info message" in caplog.text
    
    def test_logger_debug_message_not_shown_without_verbose(self, caplog):
        """Testa que DEBUG não aparece sem verbose"""
        logger = setup_logger(verbose=False)
        
        with caplog.at_level(logging.INFO, logger='pg-mirror'):
            logger.debug("Test debug message")
        
        assert "Test debug message" not in caplog.text
    
    def test_logger_debug_message_shown_with_verbose(self, caplog):
        """Testa que DEBUG aparece com verbose"""
        logger = setup_logger(verbose=True)
        
        with caplog.at_level(logging.DEBUG, logger='pg-mirror'):
            logger.debug("Test debug message")
        
        assert "Test debug message" in caplog.text
    
    def test_logger_warning_message(self, caplog):
        """Testa log de mensagem WARNING"""
        logger = setup_logger()
        
        with caplog.at_level(logging.WARNING, logger='pg-mirror'):
            logger.warning("Test warning message")
        
        assert "Test warning message" in caplog.text
    
    def test_logger_error_message(self, caplog):
        """Testa log de mensagem ERROR"""
        logger = setup_logger()
        
        with caplog.at_level(logging.ERROR, logger='pg-mirror'):
            logger.error("Test error message")
        
        assert "Test error message" in caplog.text
