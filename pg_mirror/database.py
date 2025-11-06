"""Database operations for PostgreSQL"""
import subprocess
import sys


def check_database_exists(host, port, database, user, password, logger):
    """
    Verifica se o banco de dados existe
    
    Args:
        host: Hostname do servidor PostgreSQL
        port: Porta do servidor
        database: Nome do banco de dados
        user: Usuário do PostgreSQL
        password: Senha do usuário
        logger: Logger configurado
        
    Returns:
        bool: True se o banco existe, False caso contrário
    """
    import os
    
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
        logger.debug(f"Banco '{database}' existe: {exists}")
        return exists
    except Exception as e:
        logger.error(f"Erro ao verificar existência do banco: {e}")
        return False


def create_database(host, port, database, user, password, logger):
    """
    Cria o banco de dados
    
    Args:
        host: Hostname do servidor PostgreSQL
        port: Porta do servidor
        database: Nome do banco de dados
        user: Usuário do PostgreSQL
        password: Senha do usuário
        logger: Logger configurado
    """
    import os
    
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
        logger.info(f"Banco '{database}' criado com sucesso")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao criar banco: {e.stderr.decode() if e.stderr else e}")
        sys.exit(1)


def drop_and_create_database(host, port, database, user, password, logger):
    """
    Recria o banco do zero (remove e cria novamente)
    
    Args:
        host: Hostname do servidor PostgreSQL
        port: Porta do servidor
        database: Nome do banco de dados
        user: Usuário do PostgreSQL
        password: Senha do usuário
        logger: Logger configurado
    """
    import os
    
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    
    # Termina conexões existentes
    logger.debug(f"Terminando conexões existentes no banco '{database}'")
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
        logger.debug(f"Removendo banco '{database}'")
        subprocess.run(drop_cmd, env=env, check=True, capture_output=True)
        logger.debug(f"Criando banco '{database}'")
        subprocess.run(create_cmd, env=env, check=True, capture_output=True)
        logger.info(f"Banco '{database}' recriado com sucesso")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao recriar banco: {e.stderr.decode() if e.stderr else e}")
        sys.exit(1)
