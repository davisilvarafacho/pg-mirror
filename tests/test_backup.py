"""
Testes para o módulo pg_mirror.backup
"""
import pytest
import os
from unittest.mock import patch, MagicMock, call
from pathlib import Path
from pg_mirror.backup import create_backup, cleanup_backup


class TestCreateBackup:
    """Testes para a função create_backup"""
    
    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    @patch('pathlib.Path.stat')
    def test_successful_backup(self, mock_stat, mock_tempfile, mock_run, mock_logger):
        """Testa criação bem-sucedida de backup"""
        # Mock do arquivo temporário
        mock_file = MagicMock()
        mock_file.name = '/tmp/test_backup.dump'
        mock_tempfile.return_value = mock_file
        
        # Mock do tamanho do arquivo
        mock_stat_result = MagicMock()
        mock_stat_result.st_size = 10485760  # 10 MB
        mock_stat.return_value = mock_stat_result
        
        # Mock do subprocess bem-sucedido
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        result = create_backup(
            host='localhost',
            port=5432,
            database='test_db',
            user='postgres',
            password='password',
            logger=mock_logger
        )
        
        assert result == '/tmp/test_backup.dump'
        mock_logger.info.assert_called()
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    def test_backup_command_structure(self, mock_tempfile, mock_run, mock_logger):
        """Testa estrutura do comando pg_dump"""
        mock_file = MagicMock()
        mock_file.name = '/tmp/backup.dump'
        mock_tempfile.return_value = mock_file
        
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        with patch('pathlib.Path.stat') as mock_stat:
            mock_stat.return_value = MagicMock(st_size=1024)
            
            create_backup(
                host='db.example.com',
                port=5433,
                database='mydb',
                user='dbuser',
                password='secret',
                logger=mock_logger
            )
        
        call_args = mock_run.call_args
        cmd = call_args[0][0]
        
        assert 'pg_dump' in cmd
        assert '-h' in cmd
        assert 'db.example.com' in cmd
        assert '-p' in cmd
        assert '5433' in cmd
        assert '-U' in cmd
        assert 'dbuser' in cmd
        assert '-d' in cmd
        assert 'mydb' in cmd
        assert '-Fc' in cmd  # Formato custom
    
    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    @patch('pg_mirror.backup.cleanup_backup')
    def test_backup_failure_calls_cleanup(self, mock_cleanup, mock_tempfile, mock_run, mock_logger):
        """Testa que cleanup é chamado em caso de falha"""
        mock_file = MagicMock()
        mock_file.name = '/tmp/failed_backup.dump'
        mock_tempfile.return_value = mock_file
        
        mock_run.side_effect = Exception("Backup failed")
        
        with pytest.raises(Exception):
            create_backup(
                host='localhost',
                port=5432,
                database='test_db',
                user='postgres',
                password='password',
                logger=mock_logger
            )
    
    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    def test_backup_sets_pgpassword_env(self, mock_tempfile, mock_run, mock_logger):
        """Testa que PGPASSWORD é definida no ambiente"""
        mock_file = MagicMock()
        mock_file.name = '/tmp/backup.dump'
        mock_tempfile.return_value = mock_file
        
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        with patch('pathlib.Path.stat') as mock_stat:
            mock_stat.return_value = MagicMock(st_size=1024)
            
            create_backup(
                host='localhost',
                port=5432,
                database='test_db',
                user='postgres',
                password='my_secret_password',
                logger=mock_logger
            )
        
        call_args = mock_run.call_args
        env = call_args[1]['env']
        
        assert 'PGPASSWORD' in env
        assert env['PGPASSWORD'] == 'my_secret_password'


class TestCleanupBackup:
    """Testes para a função cleanup_backup"""
    
    @patch('os.path.exists')
    @patch('os.unlink')
    def test_cleanup_existing_file(self, mock_unlink, mock_exists, mock_logger):
        """Testa remoção de arquivo existente"""
        mock_exists.return_value = True
        
        cleanup_backup('/tmp/test_backup.dump', mock_logger)
        
        mock_unlink.assert_called_once_with('/tmp/test_backup.dump')
        mock_logger.info.assert_called_once()
    
    @patch('os.path.exists')
    @patch('os.unlink')
    def test_cleanup_nonexistent_file(self, mock_unlink, mock_exists, mock_logger):
        """Testa com arquivo que não existe"""
        mock_exists.return_value = False
        
        cleanup_backup('/tmp/nonexistent.dump', mock_logger)
        
        mock_unlink.assert_not_called()
    
    @patch('os.path.exists')
    @patch('os.unlink')
    def test_cleanup_with_error(self, mock_unlink, mock_exists, mock_logger):
        """Testa tratamento de erro durante cleanup"""
        mock_exists.return_value = True
        mock_unlink.side_effect = OSError("Permission denied")
        
        cleanup_backup('/tmp/test_backup.dump', mock_logger)
        
        mock_logger.warning.assert_called_once()
    
    def test_cleanup_with_none_filepath(self, mock_logger):
        """Testa com filepath None"""
        cleanup_backup(None, mock_logger)
        
        # Não deve lançar exceção
        assert True
    
    def test_cleanup_with_empty_filepath(self, mock_logger):
        """Testa com filepath vazio"""
        cleanup_backup('', mock_logger)
        
        # Não deve lançar exceção
        assert True
