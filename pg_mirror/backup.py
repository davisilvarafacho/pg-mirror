"""Backup operations for PostgreSQL"""
import subprocess
import sys
import os
import tempfile
from pathlib import Path


def create_backup(host, port, database, user, password, logger):
    """
    Cria backup com formato custom (-Fc):
    - Compressão nativa (menor tamanho)
    - Permite restore paralelo (mais rápido)
    - Formato binário otimizado
    
    Args:
        host: Hostname do servidor PostgreSQL
        port: Porta do servidor
        database: Nome do banco de dados
        user: Usuário do PostgreSQL
        password: Senha do usuário
        logger: Logger configurado
        
    Returns:
        str: Caminho do arquivo de backup criado
    """
    # Cria arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(
        suffix='.dump',
        prefix=f'{database}_',
        delete=False
    )
    backup_path = temp_file.name
    temp_file.close()
    
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
    
    logger.info(f"Criando backup de '{database}' ({host})...")
    logger.debug(f"Usando arquivo temporário: {backup_path}")
    
    try:
        subprocess.run(
            cmd,
            env=env,
            check=True,
            capture_output=True,
            text=True
        )
        
        size_mb = Path(backup_path).stat().st_size / (1024 * 1024)
        logger.info(f"Backup criado com sucesso: {size_mb:.2f} MB")
        return backup_path
    
    except subprocess.CalledProcessError as e:
        cleanup_backup(backup_path, logger)
        logger.error(f"Erro ao criar backup: {e.stderr}")
        sys.exit(1)


def cleanup_backup(filepath, logger):
    """
    Remove arquivo temporário de backup
    
    Args:
        filepath: Caminho do arquivo a ser removido
        logger: Logger configurado
    """
    try:
        if filepath and os.path.exists(filepath):
            os.unlink(filepath)
            logger.info("Backup temporário removido")
    except Exception as e:
        logger.warning(f"Erro ao remover backup: {e}")
