#!/usr/bin/env python3
"""
pg-mirror CLI - PostgreSQL Database Mirroring Tool
"""
import sys
import click

from pg_mirror.logger import setup_logger
from pg_mirror.config import load_config
from pg_mirror.database import (
    check_database_exists,
    create_database,
    drop_and_create_database
)
from pg_mirror.backup import create_backup, cleanup_backup
from pg_mirror.restore import restore_backup
from pg_mirror.system_checks import (
    verify_system_requirements,
    SystemCheckError,
    print_installation_help
)
from pg_mirror import __version__


@click.group()
@click.version_option(version=__version__, prog_name='pg-mirror')
@click.option('-v', '--verbose', is_flag=True, help='Modo verbose (mostra mensagens DEBUG)')
@click.pass_context
def cli(ctx, verbose):
    """
    🪞 pg-mirror - PostgreSQL Database Mirroring Tool
    
    Ferramenta performática para espelhamento de bancos PostgreSQL
    com processamento paralelo e gerenciamento inteligente.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['logger'] = setup_logger(verbose)


@cli.command()
@click.option('-c', '--config', default='config.json', 
              help='Caminho para arquivo de configuração JSON')
@click.option('-j', '--jobs', type=int, 
              help='Número de jobs paralelos (sobrescreve config)')
@click.option('--drop-existing', is_flag=True, 
              help='Recriar banco se já existir (sobrescreve config)')
@click.option('--skip-checks', is_flag=True,
              help='Pular verificação de ferramentas PostgreSQL')
@click.pass_context
def mirror(ctx, config, jobs, drop_existing, skip_checks):
    """
    Espelha um banco PostgreSQL de origem para destino.
    
    Realiza backup do banco de origem e restaura no destino,
    com verificação inteligente e processamento paralelo.
    
    Exemplo:
    
        pg-mirror mirror --config config.json
        
        pg-mirror mirror -c prod-to-staging.json --jobs 8
    """
    logger = ctx.obj['logger']
    verbose = ctx.obj['verbose']
    
    # Verifica requisitos do sistema
    if not skip_checks:
        logger.info("Verificando ferramentas PostgreSQL...")
        try:
            verify_system_requirements(verbose=verbose)
            logger.info("✓ Todas as ferramentas necessárias estão instaladas")
        except SystemCheckError as e:
            logger.error(f"✗ Verificação do sistema falhou: {e}")
            logger.error("")
            print_installation_help()
            sys.exit(1)
    
    # Carrega configuração
    cfg = load_config(config, logger)
    
    # Override de opções via CLI
    if jobs:
        cfg['options']['parallel_jobs'] = jobs
    if drop_existing:
        cfg['options']['drop_existing'] = True
    
    logger.info("=" * 60)
    logger.info("Configuração carregada:")
    logger.info(f"   Origem: {cfg['source']['database']} @ {cfg['source']['host']}")
    logger.info(f"   Destino: {cfg['source']['database']} @ {cfg['target']['host']}")
    logger.info(f"   Jobs paralelos: {cfg['options']['parallel_jobs']}")
    logger.info(f"   Drop existing: {cfg['options']['drop_existing']}")
    logger.info("=" * 60)
    
    backup_file = None
    
    try:
        # 1. BACKUP
        backup_file = create_backup(
            host=cfg['source']['host'],
            port=cfg['source']['port'],
            database=cfg['source']['database'],
            user=cfg['source']['user'],
            password=cfg['source']['password'],
            logger=logger
        )
        
        # 2. PREPARAR DESTINO
        db_exists = check_database_exists(
            host=cfg['target']['host'],
            port=cfg['target']['port'],
            database=cfg['source']['database'],
            user=cfg['target']['user'],
            password=cfg['target']['password'],
            logger=logger
        )
        
        if db_exists and cfg['options']['drop_existing']:
            logger.warning(f"Recriando banco '{cfg['source']['database']}'...")
            drop_and_create_database(
                host=cfg['target']['host'],
                port=cfg['target']['port'],
                database=cfg['source']['database'],
                user=cfg['target']['user'],
                password=cfg['target']['password'],
                logger=logger
            )
        elif not db_exists:
            logger.info(f"Banco '{cfg['source']['database']}' não existe. Criando...")
            create_database(
                host=cfg['target']['host'],
                port=cfg['target']['port'],
                database=cfg['source']['database'],
                user=cfg['target']['user'],
                password=cfg['target']['password'],
                logger=logger
            )
        
        # 3. RESTORE
        success = restore_backup(
            backup_file=backup_file,
            host=cfg['target']['host'],
            port=cfg['target']['port'],
            database=cfg['source']['database'],
            user=cfg['target']['user'],
            password=cfg['target']['password'],
            parallel_jobs=cfg['options']['parallel_jobs'],
            logger=logger
        )
        
        if success:
            logger.info("=" * 60)
            logger.info("✅ Espelhamento concluído com sucesso!")
            logger.info("=" * 60)
        else:
            logger.error("=" * 60)
            logger.error("❌ Espelhamento concluído com erros")
            logger.error("=" * 60)
            sys.exit(1)
    
    finally:
        # 4. SEMPRE limpa o arquivo temporário
        if backup_file:
            cleanup_backup(backup_file, logger)


@cli.command()
@click.pass_context
def check(ctx):
    """
    Verifica se todas as ferramentas PostgreSQL estão instaladas.
    
    Verifica a presença de pg_dump, pg_restore e psql no sistema
    e exibe informações sobre versões e caminhos.
    
    Exemplo:
    
        pg-mirror check
    """
    logger = ctx.obj['logger']
    
    logger.info("Verificando ferramentas PostgreSQL...")
    logger.info("")
    
    try:
        verify_system_requirements(verbose=True)
        sys.exit(0)
    except SystemCheckError as e:
        logger.error(f"✗ Verificação falhou: {e}")
        logger.error("")
        print_installation_help()
        sys.exit(1)


@cli.command()
@click.option('-c', '--config', default='config.json',
              help='Caminho para arquivo de configuração JSON')
@click.pass_context
def validate(ctx, config):
    """
    Valida arquivo de configuração sem executar o espelhamento.
    
    Útil para verificar se o arquivo de configuração está correto
    antes de executar o espelhamento.
    
    Exemplo:
    
        pg-mirror validate --config config.json
    """
    logger = ctx.obj['logger']
    
    try:
        cfg = load_config(config, logger)
        
        logger.info("✅ Configuração válida!")
        logger.info(f"   Origem: {cfg['source']['database']} @ {cfg['source']['host']}:{cfg['source']['port']}")
        logger.info(f"   Destino: {cfg['target']['host']}:{cfg['target']['port']}")
        logger.info(f"   Opções: jobs={cfg['options']['parallel_jobs']}, drop_existing={cfg['options']['drop_existing']}")
        
    except Exception as e:
        logger.error(f"❌ Configuração inválida: {e}")
        sys.exit(1)


@cli.command()
def version():
    """Mostra a versão do pg-mirror."""
    click.echo(f"pg-mirror version {__version__}")


if __name__ == '__main__':
    cli(obj={})
