"""Restore operations for PostgreSQL"""
import subprocess
import sys
import os


def restore_backup(backup_file, host, port, database, user, password, 
                   parallel_jobs, logger):
    """
    Restore com paralelização (-j):
    - Múltiplas threads simultâneas
    - Muito mais rápido em bancos grandes
    
    Args:
        backup_file: Caminho do arquivo de backup
        host: Hostname do servidor PostgreSQL
        port: Porta do servidor
        database: Nome do banco de dados
        user: Usuário do PostgreSQL
        password: Senha do usuário
        parallel_jobs: Número de jobs paralelos
        logger: Logger configurado
        
    Returns:
        bool: True se o restore foi bem-sucedido, False caso contrário
    """
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    
    cmd = [
        'pg_restore',
        '-h', host,
        '-p', str(port),
        '-U', user,
        '-d', database,
        '-j', str(parallel_jobs),  # PARALELIZAÇÃO!
        '-v',
        '--no-owner',
        '--no-acl',
        backup_file
    ]
    
    logger.info(f"Restaurando em '{database}' ({host})...")
    logger.info(f"Usando {parallel_jobs} jobs paralelos")
    
    try:
        subprocess.run(
            cmd,
            env=env,
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("Restore concluído com sucesso!")
        return True
    
    except subprocess.CalledProcessError as e:
        logger.debug(f"Erro capturado: {e}")
        # pg_restore pode retornar 1 mesmo com sucesso (avisos)
        if "ERROR" in e.stderr:
            logger.error(f"Erro no restore: {e.stderr}")
            return False
        else:
            logger.warning("Restore concluído com avisos")
            return True
