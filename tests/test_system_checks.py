"""
Testes para o módulo pg_mirror.system_checks
"""
import pytest
from unittest.mock import patch, Mock, MagicMock
from pg_mirror.system_checks import (
    SystemCheckError,
    get_os_info,
    check_command_exists,
    get_command_version,
    check_postgresql_tools,
    get_installation_instructions,
    verify_system_requirements,
    check_python_version
)


class TestGetOsInfo:
    """Testes para get_os_info"""
    
    def test_returns_dict_with_required_keys(self):
        """Testa que retorna dicionário com chaves necessárias"""
        result = get_os_info()
        
        assert isinstance(result, dict)
        assert 'system' in result
        assert 'release' in result
        assert 'version' in result
        assert 'machine' in result
        assert 'platform' in result
    
    def test_system_field_not_empty(self):
        """Testa que campo system não está vazio"""
        result = get_os_info()
        
        assert result['system']
        assert isinstance(result['system'], str)


class TestCheckCommandExists:
    """Testes para check_command_exists"""
    
    @patch('shutil.which')
    def test_command_exists_returns_true_and_path(self, mock_which):
        """Testa quando comando existe"""
        mock_which.return_value = '/usr/bin/pg_dump'
        
        exists, path = check_command_exists('pg_dump')
        
        assert exists is True
        assert path == '/usr/bin/pg_dump'
        mock_which.assert_called_once_with('pg_dump')
    
    @patch('shutil.which')
    def test_command_not_exists_returns_false_and_none(self, mock_which):
        """Testa quando comando não existe"""
        mock_which.return_value = None
        
        exists, path = check_command_exists('nonexistent')
        
        assert exists is False
        assert path is None


class TestGetCommandVersion:
    """Testes para get_command_version"""
    
    @patch('subprocess.run')
    def test_returns_version_string(self, mock_run):
        """Testa retorno da versão quando comando é bem-sucedido"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "pg_dump (PostgreSQL) 14.5\nSome other text"
        mock_run.return_value = mock_result
        
        version = get_command_version('pg_dump')
        
        assert version == "pg_dump (PostgreSQL) 14.5"
    
    @patch('subprocess.run')
    def test_returns_none_on_error(self, mock_run):
        """Testa retorno None quando comando falha"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result
        
        version = get_command_version('nonexistent')
        
        assert version is None
    
    @patch('subprocess.run')
    def test_returns_none_on_timeout(self, mock_run):
        """Testa retorno None quando timeout"""
        mock_run.side_effect = FileNotFoundError()
        
        version = get_command_version('nonexistent')
        
        assert version is None


class TestCheckPostgresqlTools:
    """Testes para check_postgresql_tools"""
    
    @patch('pg_mirror.system_checks.check_command_exists')
    @patch('pg_mirror.system_checks.get_command_version')
    def test_all_tools_installed(self, mock_version, mock_exists):
        """Testa quando todas as ferramentas estão instaladas"""
        mock_exists.return_value = (True, '/usr/bin/tool')
        mock_version.return_value = 'Tool (PostgreSQL) 14.5'
        
        result = check_postgresql_tools()
        
        assert 'pg_dump' in result
        assert 'pg_restore' in result
        assert 'psql' in result
        
        for tool in result.values():
            assert tool['installed'] is True
            assert tool['path'] == '/usr/bin/tool'
            assert tool['version'] == 'Tool (PostgreSQL) 14.5'
    
    @patch('pg_mirror.system_checks.check_command_exists')
    @patch('pg_mirror.system_checks.get_command_version')
    def test_some_tools_missing(self, mock_version, mock_exists):
        """Testa quando algumas ferramentas estão faltando"""
        def exists_side_effect(cmd):
            if cmd == 'pg_dump':
                return (True, '/usr/bin/pg_dump')
            return (False, None)
        
        mock_exists.side_effect = exists_side_effect
        mock_version.return_value = 'pg_dump 14.5'
        
        result = check_postgresql_tools()
        
        assert result['pg_dump']['installed'] is True
        assert result['pg_restore']['installed'] is False
        assert result['psql']['installed'] is False


class TestGetInstallationInstructions:
    """Testes para get_installation_instructions"""
    
    @patch('platform.system')
    def test_returns_linux_instructions(self, mock_system):
        """Testa instruções para Linux"""
        mock_system.return_value = 'Linux'
        
        result = get_installation_instructions()
        
        assert isinstance(result, dict)
        assert 'debian' in result or 'ubuntu' in result or 'generic' in result
    
    @patch('platform.system')
    def test_returns_darwin_instructions(self, mock_system):
        """Testa instruções para macOS"""
        mock_system.return_value = 'Darwin'
        
        result = get_installation_instructions()
        
        assert isinstance(result, dict)
        assert 'homebrew' in result or 'generic' in result
    
    @patch('platform.system')
    def test_returns_windows_instructions(self, mock_system):
        """Testa instruções para Windows"""
        mock_system.return_value = 'Windows'
        
        result = get_installation_instructions()
        
        assert isinstance(result, dict)
        assert 'installer' in result or 'chocolatey' in result or 'generic' in result
    
    @patch('platform.system')
    def test_returns_generic_for_unknown_os(self, mock_system):
        """Testa instruções genéricas para SO desconhecido"""
        mock_system.return_value = 'UnknownOS'
        
        result = get_installation_instructions()
        
        assert isinstance(result, dict)
        assert 'generic' in result


class TestVerifySystemRequirements:
    """Testes para verify_system_requirements"""
    
    @patch('pg_mirror.system_checks.check_postgresql_tools')
    @patch('pg_mirror.system_checks.get_os_info')
    def test_all_requirements_met(self, mock_os_info, mock_check_tools):
        """Testa quando todos os requisitos são atendidos"""
        mock_os_info.return_value = {
            'system': 'Linux',
            'release': '5.15.0',
            'version': '',
            'machine': 'x86_64',
            'platform': 'Linux'
        }
        mock_check_tools.return_value = {
            'pg_dump': {'installed': True, 'path': '/usr/bin/pg_dump', 'version': '14.5'},
            'pg_restore': {'installed': True, 'path': '/usr/bin/pg_restore', 'version': '14.5'},
            'psql': {'installed': True, 'path': '/usr/bin/psql', 'version': '14.5'}
        }
        
        result = verify_system_requirements(verbose=False)
        
        assert result is True
    
    @patch('pg_mirror.system_checks.check_postgresql_tools')
    @patch('pg_mirror.system_checks.get_os_info')
    def test_missing_tool_raises_error(self, mock_os_info, mock_check_tools):
        """Testa que lança erro quando ferramenta está faltando"""
        mock_os_info.return_value = {'system': 'Linux', 'release': '', 'version': '', 'machine': '', 'platform': ''}
        mock_check_tools.return_value = {
            'pg_dump': {'installed': False, 'path': None, 'version': None},
            'pg_restore': {'installed': True, 'path': '/usr/bin/pg_restore', 'version': '14.5'},
            'psql': {'installed': True, 'path': '/usr/bin/psql', 'version': '14.5'}
        }
        
        with pytest.raises(SystemCheckError) as exc_info:
            verify_system_requirements(verbose=False)
        
        assert 'pg_dump' in str(exc_info.value)


class TestCheckPythonVersion:
    """Testes para check_python_version"""
    
    @patch('sys.version_info', (3, 10, 0))
    def test_python_version_sufficient(self):
        """Testa quando versão Python é suficiente"""
        result = check_python_version(min_version=(3, 8))
        
        assert result is True
    
    @patch('sys.version_info', (3, 7, 0))
    def test_python_version_insufficient_raises_error(self):
        """Testa que lança erro quando versão Python é insuficiente"""
        with pytest.raises(SystemCheckError) as exc_info:
            check_python_version(min_version=(3, 8))
        
        assert '3.8' in str(exc_info.value)
    
    @patch('sys.version_info', (3, 8, 0))
    def test_python_version_exact_match(self):
        """Testa quando versão Python é exatamente a mínima"""
        result = check_python_version(min_version=(3, 8))
        
        assert result is True


class TestSystemCheckError:
    """Testes para a exceção SystemCheckError"""
    
    def test_exception_can_be_raised(self):
        """Testa que exceção pode ser lançada"""
        with pytest.raises(SystemCheckError):
            raise SystemCheckError("Test error")
    
    def test_exception_message(self):
        """Testa mensagem da exceção"""
        with pytest.raises(SystemCheckError) as exc_info:
            raise SystemCheckError("Test error message")
        
        assert str(exc_info.value) == "Test error message"
    
    def test_exception_is_exception_subclass(self):
        """Testa que é subclasse de Exception"""
        assert issubclass(SystemCheckError, Exception)
