"""Configuration management for pg-mirror"""
import json
import sys


def load_config(config_path, logger):
    """
    Carrega e valida o arquivo JSON de configuração
    
    Args:
        config_path: Caminho para o arquivo de configuração
        logger: Logger configurado
        
    Returns:
        dict: Configuração validada
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
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
