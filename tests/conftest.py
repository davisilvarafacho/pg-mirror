"""
Configuração de fixtures e setup para testes do pg-mirror
"""
import pytest
import tempfile
import json
import os
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_logger():
    """Mock do logger para testes"""
    logger = Mock()
    logger.info = Mock()
    logger.debug = Mock()
    logger.warning = Mock()
    logger.error = Mock()
    return logger


@pytest.fixture
def valid_config():
    """Configuração válida para testes"""
    return {
        'source': {
            'host': 'source.example.com',
            'port': 5432,
            'database': 'test_db',
            'user': 'postgres',
            'password': 'secret123'
        },
        'target': {
            'host': 'target.example.com',
            'port': 5432,
            'user': 'postgres',
            'password': 'secret456'
        },
        'options': {
            'drop_existing': False,
            'parallel_jobs': 4
        }
    }


@pytest.fixture
def minimal_config():
    """Configuração mínima válida"""
    return {
        'source': {
            'host': 'localhost',
            'database': 'test_db',
            'user': 'postgres',
            'password': 'pass'
        },
        'target': {
            'host': 'localhost',
            'user': 'postgres',
            'password': 'pass'
        }
    }


@pytest.fixture
def temp_config_file(valid_config):
    """Cria arquivo temporário de configuração"""
    with tempfile.NamedTemporaryFile(
        mode='w', 
        suffix='.json', 
        delete=False
    ) as f:
        json.dump(valid_config, f)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def temp_backup_file():
    """Cria arquivo temporário de backup para testes"""
    with tempfile.NamedTemporaryFile(
        suffix='.dump',
        delete=False
    ) as f:
        f.write(b'fake backup data')
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def mock_subprocess_success():
    """Mock de subprocess.run com sucesso"""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Success"
    mock_result.stderr = ""
    return mock_result


@pytest.fixture
def mock_subprocess_error():
    """Mock de subprocess.run com erro"""
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "ERROR: Connection failed"
    return mock_result


@pytest.fixture
def mock_os_info_linux():
    """Mock de informações do OS para Linux"""
    return {
        "system": "Linux",
        "release": "5.15.0",
        "version": "#1 SMP",
        "machine": "x86_64",
        "platform": "Linux-5.15.0-x86_64"
    }


@pytest.fixture
def mock_os_info_darwin():
    """Mock de informações do OS para macOS"""
    return {
        "system": "Darwin",
        "release": "21.6.0",
        "version": "Darwin Kernel Version 21.6.0",
        "machine": "x86_64",
        "platform": "macOS-12.5-x86_64"
    }


@pytest.fixture
def mock_os_info_windows():
    """Mock de informações do OS para Windows"""
    return {
        "system": "Windows",
        "release": "10",
        "version": "10.0.19045",
        "machine": "AMD64",
        "platform": "Windows-10-10.0.19045"
    }
