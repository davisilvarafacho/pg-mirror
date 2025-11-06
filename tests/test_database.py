"""
Testes para o módulo pg_mirror.database
"""
import pytest
from unittest.mock import patch, MagicMock
from pg_mirror.database import (
    check_database_exists,
    create_database,
    drop_and_create_database
)


class TestCheckDatabaseExists:
    """Testes para check_database_exists"""
    
    @patch('subprocess.run')
    def test_database_exists_returns_true(self, mock_run, mock_logger):
        """Testa quando banco existe"""
        mock_result = MagicMock()
        mock_result.stdout = '1'
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        result = check_database_exists(
            host='localhost',
            port=5432,
            database='existing_db',
            user='postgres',
            password='password',
            logger=mock_logger
        )
        
        assert result is True
    
    @patch('subprocess.run')
    def test_database_not_exists_returns_false(self, mock_run, mock_logger):
        """Testa quando banco não existe"""
        mock_result = MagicMock()
        mock_result.stdout = ''
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        result = check_database_exists(
            host='localhost',
            port=5432,
            database='nonexistent_db',
            user='postgres',
            password='password',
            logger=mock_logger
        )
        
        assert result is False
    
    @patch('subprocess.run')
    def test_check_database_command_structure(self, mock_run, mock_logger):
        """Testa estrutura do comando psql"""
        mock_result = MagicMock()
        mock_result.stdout = '1'
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        check_database_exists(
            host='db.example.com',
            port=5433,
            database='test_db',
            user='dbuser',
            password='secret',
            logger=mock_logger
        )
        
        call_args = mock_run.call_args
        cmd = call_args[0][0]
        
        assert 'psql' in cmd
        assert '-h' in cmd
        assert 'db.example.com' in cmd
        assert '-p' in cmd
        assert '5433' in cmd
        assert '-U' in cmd
        assert 'dbuser' in cmd
        assert '-d' in cmd
        assert 'postgres' in cmd  # Conecta ao postgres para verificar
        assert '-tAc' in cmd
    
    @patch('subprocess.run')
    def test_check_database_exception_returns_false(self, mock_run, mock_logger):
        """Testa que retorna False em caso de exceção"""
        mock_run.side_effect = Exception("Connection failed")
        
        result = check_database_exists(
            host='localhost',
            port=5432,
            database='test_db',
            user='postgres',
            password='password',
            logger=mock_logger
        )
        
        assert result is False
        mock_logger.error.assert_called_once()


class TestCreateDatabase:
    """Testes para create_database"""
    
    @patch('subprocess.run')
    def test_create_database_success(self, mock_run, mock_logger):
        """Testa criação bem-sucedida de banco"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        create_database(
            host='localhost',
            port=5432,
            database='new_db',
            user='postgres',
            password='password',
            logger=mock_logger
        )
        
        mock_logger.info.assert_called_once()
        assert 'criado com sucesso' in str(mock_logger.info.call_args)
    
    @patch('subprocess.run')
    def test_create_database_command_structure(self, mock_run, mock_logger):
        """Testa estrutura do comando CREATE DATABASE"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        create_database(
            host='db.example.com',
            port=5433,
            database='my_new_db',
            user='dbuser',
            password='secret',
            logger=mock_logger
        )
        
        call_args = mock_run.call_args
        cmd = call_args[0][0]
        
        assert 'psql' in cmd
        assert '-h' in cmd
        assert 'db.example.com' in cmd
        assert '-c' in cmd
        # Verifica se o comando SQL está presente
        assert any('CREATE DATABASE' in arg for arg in cmd)
    
    @patch('subprocess.run')
    def test_create_database_failure_exits(self, mock_run, mock_logger):
        """Testa que falha sai do programa"""
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(
            returncode=1,
            cmd=['psql'],
            stderr=b"CREATE failed"
        )
        
        with pytest.raises(SystemExit):
            create_database(
                host='localhost',
                port=5432,
                database='new_db',
                user='postgres',
                password='password',
                logger=mock_logger
            )
        
        mock_logger.error.assert_called_once()


class TestDropAndCreateDatabase:
    """Testes para drop_and_create_database"""
    
    @patch('subprocess.run')
    def test_drop_and_create_success(self, mock_run, mock_logger):
        """Testa drop e create bem-sucedidos"""
        # Todos os comandos são bem-sucedidos
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        drop_and_create_database(
            host='localhost',
            port=5432,
            database='test_db',
            user='postgres',
            password='password',
            logger=mock_logger
        )
        
        # Deve ter chamado subprocess múltiplas vezes
        # (terminate connections, drop, create)
        assert mock_run.call_count >= 2
    
    @patch('subprocess.run')
    def test_drop_and_create_terminates_connections(self, mock_run, mock_logger):
        """Testa que conexões são terminadas antes do drop"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        drop_and_create_database(
            host='localhost',
            port=5432,
            database='test_db',
            user='postgres',
            password='password',
            logger=mock_logger
        )
        
        # Verifica se algum comando contém pg_terminate_backend
        calls = [str(call) for call in mock_run.call_args_list]
        has_terminate = any('pg_terminate_backend' in call for call in calls)
        assert has_terminate
    
    @patch('subprocess.run')
    def test_drop_database_command_present(self, mock_run, mock_logger):
        """Testa que comando DROP DATABASE está presente"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        drop_and_create_database(
            host='localhost',
            port=5432,
            database='test_db',
            user='postgres',
            password='password',
            logger=mock_logger
        )
        
        # Verifica se algum comando contém DROP DATABASE
        calls = [str(call) for call in mock_run.call_args_list]
        has_drop = any('DROP DATABASE' in call for call in calls)
        assert has_drop
    
    @patch('subprocess.run')
    def test_drop_and_create_failure_exits(self, mock_run, mock_logger):
        """Testa que falha sai do programa"""
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(
            returncode=1,
            cmd=['psql'],
            stderr=b"DROP failed"
        )
        
        with pytest.raises(SystemExit):
            drop_and_create_database(
                host='localhost',
                port=5432,
                database='test_db',
                user='postgres',
                password='password',
                logger=mock_logger
            )
        
        mock_logger.error.assert_called()
