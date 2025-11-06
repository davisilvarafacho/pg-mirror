# System Checks - Verificação de Requisitos do Sistema

O pg-mirror inclui um sistema robusto de verificação de requisitos que garante que todas as ferramentas necessárias estejam instaladas antes de executar operações de espelhamento de banco de dados.

## 🎯 Objetivo

O sistema de verificação (system checks) automaticamente detecta e valida:

- ✅ Presença das ferramentas PostgreSQL client (`pg_dump`, `pg_restore`, `psql`)
- ✅ Versões das ferramentas instaladas
- ✅ Caminhos de instalação
- ✅ Sistema operacional (Linux, macOS, Windows)
- ✅ Versão do Python

## 🔍 Como Funciona

### Verificação Automática

Por padrão, o comando `mirror` executa verificação automática:

```bash
pg-mirror mirror --config config.json
```

**Saída:**
```
INFO - Verificando ferramentas PostgreSQL...
INFO - ✓ Todas as ferramentas necessárias estão instaladas
```

### Verificação Manual

Use o comando `check` para verificar o sistema a qualquer momento:

```bash
pg-mirror check
```

**Saída detalhada:**
```
============================================================
System Information:
============================================================
OS: Linux 6.14.0-33-generic
Platform: Linux-6.14.0-33-generic-x86_64-with-glibc2.39
Machine: x86_64

============================================================
PostgreSQL Client Tools:
============================================================
✓ pg_dump      : pg_dump (PostgreSQL) 16.10
  Path: /usr/bin/pg_dump
✓ pg_restore   : pg_restore (PostgreSQL) 16.10
  Path: /usr/bin/pg_restore
✓ psql         : psql (PostgreSQL) 16.10
  Path: /usr/bin/psql

============================================================
✓ All system requirements met!
============================================================
```

### Pular Verificação

Em ambientes onde você tem certeza que as ferramentas estão instaladas:

```bash
pg-mirror mirror --config config.json --skip-checks
```

## 🛠️ Instalação de Ferramentas

Se a verificação falhar, o pg-mirror exibe automaticamente instruções específicas para seu sistema operacional.

### Linux

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install postgresql-client
```

#### Fedora/RHEL/CentOS
```bash
sudo dnf install postgresql
# ou
sudo yum install postgresql
```

#### Arch Linux
```bash
sudo pacman -S postgresql
```

### macOS

#### Homebrew (recomendado)
```bash
brew install postgresql
```

#### MacPorts
```bash
sudo port install postgresql-client
```

### Windows

#### Instalador Oficial
1. Baixe em: https://www.postgresql.org/download/windows/
2. Durante instalação, selecione "Command Line Tools"
3. Adicione ao PATH: `C:\Program Files\PostgreSQL\XX\bin`

#### Chocolatey
```bash
choco install postgresql
```

#### Scoop
```bash
scoop install postgresql
```

## 📋 Verificação de Instalação

Após instalar, verifique manualmente:

```bash
pg_dump --version
pg_restore --version
psql --version
```

Ou use o pg-mirror:

```bash
pg-mirror check
```

## 🔧 Módulo system_checks.py

O módulo `pg_mirror/system_checks.py` fornece as seguintes funções:

### `check_postgresql_tools()`

Verifica se todas as ferramentas necessárias estão instaladas.

```python
from pg_mirror.system_checks import check_postgresql_tools

tools = check_postgresql_tools()
# Retorna:
# {
#     'pg_dump': {'installed': True, 'path': '/usr/bin/pg_dump', 'version': '...'},
#     'pg_restore': {'installed': True, 'path': '/usr/bin/pg_restore', 'version': '...'},
#     'psql': {'installed': True, 'path': '/usr/bin/psql', 'version': '...'}
# }
```

### `verify_system_requirements(verbose=False)`

Verifica todos os requisitos do sistema. Lança `SystemCheckError` se algum requisito faltar.

```python
from pg_mirror.system_checks import verify_system_requirements, SystemCheckError

try:
    verify_system_requirements(verbose=True)
    print("Sistema OK!")
except SystemCheckError as e:
    print(f"Erro: {e}")
```

### `get_os_info()`

Retorna informações sobre o sistema operacional:

```python
from pg_mirror.system_checks import get_os_info

os_info = get_os_info()
# Retorna:
# {
#     'system': 'Linux',      # ou 'Darwin' (macOS), 'Windows'
#     'release': '6.14.0-33-generic',
#     'version': '...',
#     'machine': 'x86_64',
#     'platform': 'Linux-6.14.0-33-generic-x86_64-with-glibc2.39'
# }
```

### `get_installation_instructions()`

Retorna instruções de instalação específicas para o SO atual:

```python
from pg_mirror.system_checks import get_installation_instructions

instructions = get_installation_instructions()
# Retorna dict com comandos de instalação por método
```

### `check_python_version(min_version=(3, 8))`

Verifica se a versão do Python atende aos requisitos mínimos:

```python
from pg_mirror.system_checks import check_python_version

check_python_version(min_version=(3, 8))  # Lança SystemCheckError se < 3.8
```

## 🚨 Tratamento de Erros

### SystemCheckError

Exceção lançada quando verificações do sistema falham:

```python
from pg_mirror.system_checks import SystemCheckError

try:
    # alguma operação
    pass
except SystemCheckError as e:
    print(f"Erro de sistema: {e}")
    # Exibir instruções de instalação
```

### Exemplo de erro

Se `pg_dump` não estiver instalado:

```
✗ pg_dump      : NOT FOUND

Missing required PostgreSQL client tools: pg_dump

Installation Instructions:
============================================================

UBUNTU/DEBIAN:
  sudo apt-get update && sudo apt-get install postgresql-client

FEDORA/RHEL:
  sudo dnf install postgresql
```

## 🎨 Integração no CLI

O CLI integra verificação de sistema no fluxo:

```python
# Em pg_mirror/cli.py

@cli.command()
@click.option('--skip-checks', is_flag=True, help='Pular verificação')
@click.pass_context
def mirror(ctx, config, skip_checks):
    if not skip_checks:
        try:
            verify_system_requirements(verbose=verbose)
            logger.info("✓ Ferramentas OK")
        except SystemCheckError as e:
            logger.error(f"✗ Verificação falhou: {e}")
            print_installation_help()
            sys.exit(1)
    # ... continua com espelhamento
```

## 💡 Boas Práticas

1. **Execute `pg-mirror check` primeiro** ao configurar um novo ambiente
2. **Use `--skip-checks`** apenas em ambientes conhecidos/confiáveis
3. **Mantenha as ferramentas atualizadas** para melhor compatibilidade
4. **Verifique logs** se encontrar problemas de execução

## 🔗 Referências

- [Documentação PostgreSQL Client Tools](https://www.postgresql.org/docs/current/app-pgdump.html)
- [Python platform module](https://docs.python.org/3/library/platform.html)
- [Python shutil module](https://docs.python.org/3/library/shutil.html)

## � Documentação Relacionada

- [Guia Rápido](QUICKSTART.md)
- [Referência CLI](../reference/README_CLI.md)
- [Guia de Instalação](../installation.md)
- [Voltar para Documentação](../README.md)

## �📝 Changelog

- **v1.0.0**: Sistema de verificação inicial com suporte para Linux, macOS e Windows
