"""
Testes para o módulo pg_mirror.restore
"""
import pytest
from unittest.mock import patch, MagicMock
from pg_mirror.restore import restore_backup


class TestRestoreBackup:
    """Testes para restore_backup"""
    
    @patch('subprocess.run')
    def test_successful_restore(self, mock_run, mock_logger):
        """Testa restore bem-sucedido"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        result = restore_backup(
            backup_file='/tmp/backup.dump',
            host='localhost',
            port=5432,
            database='test_db',
            user='postgres',
            password='password',
            parallel_jobs=4,
            logger=mock_logger
        )
        
        assert result is True
        mock_logger.info.assert_called()
    
    @patch('subprocess.run')
    def test_restore_command_structure(self, mock_run, mock_logger):
        """Testa estrutura do comando pg_restore"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        restore_backup(
            backup_file='/tmp/backup.dump',
            host='db.example.com',
            port=5433,
            database='mydb',
            user='dbuser',
            password='secret',
            parallel_jobs=8,
            logger=mock_logger
        )
        
        call_args = mock_run.call_args
        cmd = call_args[0][0]
        
        assert 'pg_restore' in cmd
        assert '-h' in cmd
        assert 'db.example.com' in cmd
        assert '-p' in cmd
        assert '5433' in cmd
        assert '-U' in cmd
        assert 'dbuser' in cmd
        assert '-d' in cmd
        assert 'mydb' in cmd
        assert '-j' in cmd  # Parallel jobs
        assert '8' in cmd
        assert '--no-owner' in cmd
        assert '--no-acl' in cmd
        assert '/tmp/backup.dump' in cmd
    
    @patch('subprocess.run')
    def test_restore_with_warnings_succeeds(self, mock_run, mock_logger):
        """Testa que restore com avisos ainda é considerado sucesso"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "WARNING: some non-critical warning"
        mock_run.return_value = mock_result
        
        # Força exceção mas sem ERROR no stderr
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(
            returncode=1,
            cmd=['pg_restore'],
            stderr="WARNING: some warning"
        )
        
        result = restore_backup(
            backup_file='/tmp/backup.dump',
            host='localhost',
            port=5432,
            database='test_db',
            user='postgres',
            password='password',
            parallel_jobs=4,
            logger=mock_logger
        )
        
        assert result is True
        mock_logger.warning.assert_called()
    
    @patch('subprocess.run')
    def test_restore_with_error_fails(self, mock_run, mock_logger):
        """Testa que restore com erro falha"""
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(
            returncode=1,
            cmd=['pg_restore'],
            stderr="ERROR: connection failed"
        )
        
        result = restore_backup(
            backup_file='/tmp/backup.dump',
            host='localhost',
            port=5432,
            database='test_db',
            user='postgres',
            password='password',
            parallel_jobs=4,
            logger=mock_logger
        )
        
        assert result is False
        mock_logger.error.assert_called()
    
    @patch('subprocess.run')
    def test_restore_sets_pgpassword_env(self, mock_run, mock_logger):
        """Testa que PGPASSWORD é definida no ambiente"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        restore_backup(
            backup_file='/tmp/backup.dump',
            host='localhost',
            port=5432,
            database='test_db',
            user='postgres',
            password='my_secret_password',
            parallel_jobs=4,
            logger=mock_logger
        )
        
        call_args = mock_run.call_args
        env = call_args[1]['env']
        
        assert 'PGPASSWORD' in env
        assert env['PGPASSWORD'] == 'my_secret_password'
    
    @patch('subprocess.run')
    def test_restore_uses_parallel_jobs(self, mock_run, mock_logger):
        """Testa que número de jobs paralelos é usado"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        restore_backup(
            backup_file='/tmp/backup.dump',
            host='localhost',
            port=5432,
            database='test_db',
            user='postgres',
            password='password',
            parallel_jobs=16,
            logger=mock_logger
        )
        
        call_args = mock_run.call_args
        cmd = call_args[0][0]
        
        assert '-j' in cmd
        assert '16' in cmd
    
    @patch('subprocess.run')
    def test_restore_logs_parallel_jobs_info(self, mock_run, mock_logger):
        """Testa que informa quantidade de jobs paralelos no log"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        restore_backup(
            backup_file='/tmp/backup.dump',
            host='localhost',
            port=5432,
            database='test_db',
            user='postgres',
            password='password',
            parallel_jobs=4,
            logger=mock_logger
        )
        
        # Verifica se logger.info foi chamado com informação de jobs
        info_calls = [str(call) for call in mock_logger.info.call_args_list]
        has_jobs_info = any('4' in call and 'jobs' in call.lower() for call in info_calls)
        assert has_jobs_info
