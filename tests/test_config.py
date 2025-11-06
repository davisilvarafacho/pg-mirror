"""
Testes para o módulo pg_mirror.config
"""
import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch
from pg_mirror.config import load_config


class TestLoadConfig:
    """Testes para a função load_config"""
    
    def test_load_valid_config(self, temp_config_file, mock_logger):
        """Testa carregamento de configuração válida"""
        config = load_config(temp_config_file, mock_logger)
        
        assert config['source']['host'] == 'source.example.com'
        assert config['source']['database'] == 'test_db'
        assert config['target']['host'] == 'target.example.com'
        assert config['options']['parallel_jobs'] == 4
    
    def test_load_minimal_config_with_defaults(self, minimal_config, mock_logger):
        """Testa configuração mínima com valores padrão"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(minimal_config, f)
            temp_path = f.name
        
        try:
            config = load_config(temp_path, mock_logger)
            
            # Verifica valores padrão
            assert config['source']['port'] == 5432
            assert config['target']['port'] == 5432
            assert config['options']['drop_existing'] is False
            assert config['options']['parallel_jobs'] == 4
        finally:
            os.unlink(temp_path)
    
    def test_missing_config_file(self, mock_logger):
        """Testa erro quando arquivo não existe"""
        with pytest.raises(SystemExit):
            load_config('nonexistent_file.json', mock_logger)
        
        mock_logger.error.assert_called_once()
        assert 'não encontrado' in str(mock_logger.error.call_args)
    
    def test_invalid_json(self, mock_logger):
        """Testa erro com JSON inválido"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json }")
            temp_path = f.name
        
        try:
            with pytest.raises(SystemExit):
                load_config(temp_path, mock_logger)
            
            mock_logger.error.assert_called_once()
            assert 'parsear JSON' in str(mock_logger.error.call_args)
        finally:
            os.unlink(temp_path)
    
    def test_missing_source_section(self, mock_logger):
        """Testa erro quando seção source está faltando"""
        config = {'target': {'host': 'localhost', 'user': 'postgres', 'password': 'pass'}}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name
        
        try:
            with pytest.raises(SystemExit):
                load_config(temp_path, mock_logger)
            
            mock_logger.error.assert_called_once()
            assert 'source' in str(mock_logger.error.call_args)
        finally:
            os.unlink(temp_path)
    
    def test_missing_required_field_source_host(self, mock_logger):
        """Testa erro quando campo obrigatório source.host está faltando"""
        config = {
            'source': {'database': 'db', 'user': 'user', 'password': 'pass'},
            'target': {'host': 'localhost', 'user': 'postgres', 'password': 'pass'}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name
        
        try:
            with pytest.raises(SystemExit):
                load_config(temp_path, mock_logger)
            
            mock_logger.error.assert_called_once()
            assert 'source.host' in str(mock_logger.error.call_args)
        finally:
            os.unlink(temp_path)
    
    def test_missing_required_field_source_database(self, mock_logger):
        """Testa erro quando source.database está faltando"""
        config = {
            'source': {'host': 'localhost', 'user': 'user', 'password': 'pass'},
            'target': {'host': 'localhost', 'user': 'postgres', 'password': 'pass'}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name
        
        try:
            with pytest.raises(SystemExit):
                load_config(temp_path, mock_logger)
            
            assert 'source.database' in str(mock_logger.error.call_args)
        finally:
            os.unlink(temp_path)
    
    def test_custom_port_values(self, mock_logger):
        """Testa configuração com portas customizadas"""
        config = {
            'source': {
                'host': 'localhost',
                'port': 5433,
                'database': 'db',
                'user': 'user',
                'password': 'pass'
            },
            'target': {
                'host': 'localhost',
                'port': 5434,
                'user': 'postgres',
                'password': 'pass'
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name
        
        try:
            result = load_config(temp_path, mock_logger)
            
            assert result['source']['port'] == 5433
            assert result['target']['port'] == 5434
        finally:
            os.unlink(temp_path)
    
    def test_custom_options(self, mock_logger):
        """Testa configuração com opções customizadas"""
        config = {
            'source': {
                'host': 'localhost',
                'database': 'db',
                'user': 'user',
                'password': 'pass'
            },
            'target': {
                'host': 'localhost',
                'user': 'postgres',
                'password': 'pass'
            },
            'options': {
                'drop_existing': True,
                'parallel_jobs': 8
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name
        
        try:
            result = load_config(temp_path, mock_logger)
            
            assert result['options']['drop_existing'] is True
            assert result['options']['parallel_jobs'] == 8
        finally:
            os.unlink(temp_path)
