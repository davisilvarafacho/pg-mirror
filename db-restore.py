#!/usr/bin/env python3
import subprocess
import os
import sys
import json
import tempfile
from pathlib import Path
import argparse
import logging


def setup_logger():
    """Configura o logger da aplicação"""
    logger = logging.getLogger('PostgresBackupRestore')
    logger.setLevel(logging.DEBUG)
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Formato detalhado
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    return logger


class PostgresBackupRestore:
    def __init__(self, parallel_jobs=4, logger=None):
        self.parallel_jobs = parallel_jobs
        self.temp_file = None
        self.logger = logger or logging.getLogger('PostgresBackupRestore')
    
    def create_backup(self, host, port, database, user, password):
        """
        Cria backup com formato custom (-Fc):
        - Compressão nativa (menor tamanho)
        - Permite restore paralelo (mais rápido)
        - Formato binário otimizado
        """

        # Cria arquivo temporário que será auto-deletado
        self.temp_file = tempfile.NamedTemporaryFile(
            suffix='.dump',
            prefix=f'{database}_',
            delete=False  # Vamos controlar a deleção manualmente
        )
        backup_path = self.temp_file.name
        self.temp_file.close()  # Fecha para pg_dump poder escrever
        
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        cmd = [
            'pg_dump',
            '-h', host,
            '-p', str(port),
            '-U', user,
            '-d', database,
            '-Fc',  # Formato Custom (compactado e performático)
            '-Z', '6',  # Nível de compressão (0-9, 6 é bom balanço)
            '-b',  # Include large objects
            '-v',  # Verbose
            '-f', backup_path
        ]
        
        self.logger.info(f"Criando backup de '{database}' ({host})...")
        self.logger.debug(f"Usando arquivo temporário: {backup_path}")
        
        try:
            subprocess.run(
                cmd,
                env=env,
                check=True,
                capture_output=True,
                text=True
            )
            
            size_mb = Path(backup_path).stat().st_size / (1024 * 1024)
            self.logger.info(f"Backup criado com sucesso: {size_mb:.2f} MB")
            return backup_path
        
        except subprocess.CalledProcessError as e:
            self._cleanup(backup_path)
            self.logger.error(f"Erro ao criar backup: {e.stderr}")
            sys.exit(1)
    
    def restore_backup(self, backup_file, host, port, database, user, password, 
                       drop_existing=False):
        """
        Restore com paralelização (-j):
        - Múltiplas threads simultâneas
        - Muito mais rápido em bancos grandes
        - Analogia: ao invés de 1 pessoa desempacotando, várias trabalham juntas
        """
        
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        # Verifica se o banco existe
        db_exists = self._check_database_exists(host, port, database, user, password)
        
        if db_exists and drop_existing:
            self.logger.warning(f"Recriando banco '{database}'...")
            self._drop_and_create_db(host, port, database, user, password)
        elif not db_exists:
            self.logger.info(f"Banco '{database}' não existe. Criando...")
            self._create_db(host, port, database, user, password)
        
        cmd = [
            'pg_restore',
            '-h', host,
            '-p', str(port),
            '-U', user,
            '-d', database,
            '-j', str(self.parallel_jobs),  # PARALELIZAÇÃO!
            '-v',
            '--no-owner',
            '--no-acl',
            backup_file
        ]
        
        self.logger.info(f"Restaurando em '{database}' ({host})...")
        self.logger.info(f"Usando {self.parallel_jobs} jobs paralelos")
        
        try:
            subprocess.run(
                cmd,
                env=env,
                check=True,
                capture_output=True,
                text=True
            )
            self.logger.info("Restore concluído com sucesso!")
            return True
        
        except subprocess.CalledProcessError as e:
            self.logger.debug(f"Erro capturado: {e}")
            # pg_restore pode retornar 1 mesmo com sucesso (avisos)
            if "ERROR" in e.stderr:
                self.logger.error(f"Erro no restore: {e.stderr}")
                return False
            else:
                self.logger.warning("Restore concluído com avisos")
                return True
    
    def _check_database_exists(self, host, port, database, user, password):
        """Verifica se o banco de dados existe"""
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        check_cmd = [
            'psql',
            '-h', host,
            '-p', str(port),
            '-U', user,
            '-d', 'postgres',
            '-tAc', f"SELECT 1 FROM pg_database WHERE datname='{database}';"
        ]
        
        try:
            result = subprocess.run(
                check_cmd,
                env=env,
                capture_output=True,
                text=True,
                check=False
            )
            exists = result.stdout.strip() == '1'
            self.logger.debug(f"Banco '{database}' existe: {exists}")
            return exists
        except Exception as e:
            self.logger.error(f"Erro ao verificar existência do banco: {e}")
            return False
    
    def _create_db(self, host, port, database, user, password):
        """Cria o banco de dados"""

        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        create_cmd = [
            'psql',
            '-h', host,
            '-p', str(port),
            '-U', user,
            '-d', 'postgres',
            '-c', f'CREATE DATABASE "{database}";'
        ]
        
        try:
            subprocess.run(create_cmd, env=env, check=True, capture_output=True)
            self.logger.info(f"Banco '{database}' criado com sucesso")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Erro ao criar banco: {e.stderr.decode() if e.stderr else e}")
            sys.exit(1)
    
    def _drop_and_create_db(self, host, port, database, user, password):
        """Recria o banco do zero"""
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        # Termina conexões existentes
        self.logger.debug(f"Terminando conexões existentes no banco '{database}'")
        terminate_cmd = [
            'psql',
            '-h', host,
            '-p', str(port),
            '-U', user,
            '-d', 'postgres',
            '-c', f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{database}'
                AND pid <> pg_backend_pid();
            """
        ]
        
        drop_cmd = [
            'psql',
            '-h', host,
            '-p', str(port),
            '-U', user,
            '-d', 'postgres',
            '-c', f'DROP DATABASE IF EXISTS "{database}";'
        ]
        
        create_cmd = [
            'psql',
            '-h', host,
            '-p', str(port),
            '-U', user,
            '-d', 'postgres',
            '-c', f'CREATE DATABASE "{database}";'
        ]
        
        try:
            subprocess.run(terminate_cmd, env=env, capture_output=True)
            self.logger.debug(f"Removendo banco '{database}'")
            subprocess.run(drop_cmd, env=env, check=True, capture_output=True)
            self.logger.debug(f"Criando banco '{database}'")
            subprocess.run(create_cmd, env=env, check=True, capture_output=True)
            self.logger.info(f"Banco '{database}' recriado com sucesso")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Erro ao recriar banco: {e.stderr.decode() if e.stderr else e}")
            sys.exit(1)
    
    def _cleanup(self, filepath):
        """Remove arquivo temporário"""
        try:
            if filepath and os.path.exists(filepath):
                os.unlink(filepath)
                self.logger.info("Backup temporário removido")
        except Exception as e:
            self.logger.warning(f"Erro ao remover backup: {e}")


def load_config(config_path, logger):
    """Carrega e valida o arquivo JSON"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Valida campos obrigatórios
        required_fields = {
            'source': ['host', 'database', 'user', 'password'],
            'target': ['host', 'user', 'password']
        }
        
        for section, fields in required_fields.items():
            if section not in config:
                raise ValueError(f"Seção '{section}' não encontrada no JSON")
            for field in fields:
                if field not in config[section]:
                    raise ValueError(f"Campo '{section}.{field}' obrigatório")
        
        # Define valores padrão
        config['source'].setdefault('port', 5432)
        config['target'].setdefault('port', 5432)
        config.setdefault('options', {})
        config['options'].setdefault('drop_existing', False)
        config['options'].setdefault('parallel_jobs', 4)
        
        return config
    
    except FileNotFoundError:
        logger.error(f"Arquivo de configuração não encontrado: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao parsear JSON: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Configuração inválida: {e}")
        sys.exit(1)


def main():
    # Configura o logger
    logger = setup_logger()
    
    parser = argparse.ArgumentParser(
        description='Backup e Restore PostgreSQL entre servidores (performático)'
    )
    parser.add_argument(
        '--config',
        default='config.json',
        help='Caminho para arquivo de configuração JSON'
    )
    
    args = parser.parse_args()
    
    # Carrega configurações
    config = load_config(args.config, logger)
    
    logger.info("=" * 60)
    logger.info("Configuração carregada:")
    logger.info(f"   Origem: {config['source']['database']} @ {config['source']['host']}")
    logger.info(f"   Destino: {config['source']['database']} @ {config['target']['host']}")
    logger.info(f"   Jobs paralelos: {config['options']['parallel_jobs']}")
    logger.info(f"   Drop existing: {config['options']['drop_existing']}")
    logger.info("=" * 60)
    
    # Inicializa
    backup_restore = PostgresBackupRestore(
        parallel_jobs=config['options']['parallel_jobs'],
        logger=logger
    )
    
    backup_file = None
    
    try:
        # 1. BACKUP
        backup_file = backup_restore.create_backup(
            host=config['source']['host'],
            port=config['source']['port'],
            database=config['source']['database'],
            user=config['source']['user'],
            password=config['source']['password']
        )
        
        # 2. RESTORE
        success = backup_restore.restore_backup(
            backup_file=backup_file,
            host=config['target']['host'],
            port=config['target']['port'],
            database=config['source']['database'],  # Mesmo nome!
            user=config['target']['user'],
            password=config['target']['password'],
            drop_existing=config['options']['drop_existing']
        )
        
        if success:
            logger.info("=" * 60)
            logger.info("Migração concluída com sucesso!")
            logger.info("=" * 60)
        else:
            logger.error("=" * 60)
            logger.error("Migração concluída com erros")
            logger.error("=" * 60)
            sys.exit(1)
    
    finally:
        # 3. SEMPRE limpa o arquivo temporário
        if backup_file:
            backup_restore._cleanup(backup_file)


if __name__ == "__main__":
    main()
