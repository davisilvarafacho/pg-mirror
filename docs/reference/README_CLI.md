# 🪞 pg-mirror - PostgreSQL Database Mirroring Tool (CLI)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Uma ferramenta CLI performática para espelhamento (mirror) de bancos de dados PostgreSQL entre servidores, com suporte a processamento paralelo e gerenciamento inteligente de bancos.

## ✨ Características

- 🚀 **Backup paralelo**: Utiliza formato custom do PostgreSQL com compressão nativa
- ⚡ **Restore multi-threaded**: Restauração até 4x mais rápida com jobs paralelos
- 🔍 **Verificação inteligente**: Detecta se o banco existe antes de restaurar
- 🛡️ **Seguro**: Gerenciamento automático de conexões e arquivos temporários
- 📝 **Logging estruturado**: Acompanhamento detalhado de cada operação
- ⚙️ **Configuração JSON**: Setup simples via arquivo de configuração
- 💻 **CLI moderna**: Interface de linha de comando intuitiva com Click

## 📦 Estrutura do Projeto

```
pg-mirror/
├── pg_mirror/              # Pacote principal
│   ├── __init__.py
│   ├── cli.py             # CLI principal (Click)
│   ├── backup.py          # Operações de backup
│   ├── restore.py         # Operações de restore
│   ├── database.py        # Gerenciamento de banco
│   ├── config.py          # Configuração
│   └── logger.py          # Sistema de logging
├── examples/              # Exemplos de configuração
├── tests/                 # Testes unitários
├── pg-mirror              # Script executável
└── pyproject.toml         # Configuração do projeto
```

## 📋 Requisitos

- Python 3.8+
- PostgreSQL client tools (`pg_dump`, `pg_restore`, `psql`)
- Acesso aos servidores de origem e destino

## 🔧 Instalação

### Via pip (quando publicado no PyPI)

```bash
pip install pg-mirror
```

### Via clone do repositório

```bash
git clone https://github.com/seu-usuario/pg-mirror.git
cd pg-mirror
pip install -r requirements.txt

# Instalar em modo desenvolvimento
pip install -e .
```

### Instalar PostgreSQL client tools

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql-client
```

**macOS:**
```bash
brew install postgresql
```

## 🚀 Uso

### Comandos Disponíveis

```bash
# Ver ajuda geral
pg-mirror --help

# Verificar ferramentas PostgreSQL instaladas
pg-mirror check

# Espelhar banco de dados
pg-mirror mirror --config config.json

# Validar configuração
pg-mirror validate --config config.json

# Ver versão
pg-mirror version
```

### Verificação de Requisitos

Antes de usar o pg-mirror, certifique-se de que as ferramentas PostgreSQL estão instaladas:

```bash
# Verificar instalação
pg-mirror check
```

Este comando verifica:
- ✓ `pg_dump` - Para criar backups
- ✓ `pg_restore` - Para restaurar backups
- ✓ `psql` - Para gerenciar bancos de dados

Se alguma ferramenta estiver faltando, o comando exibirá instruções de instalação específicas para seu sistema operacional (Linux, macOS, Windows).

### 1. Criar arquivo de configuração

```bash
cp examples/config.example.json config.json
# Edite config.json com suas credenciais
```

Exemplo de `config.json`:

```json
{
  "source": {
    "host": "origem.exemplo.com",
    "port": 5432,
    "database": "meu_banco",
    "user": "postgres",
    "password": "senha_segura"
  },
  "target": {
    "host": "destino.exemplo.com",
    "port": 5432,
    "user": "postgres",
    "password": "senha_segura"
  },
  "options": {
    "drop_existing": false,
    "parallel_jobs": 4
  }
}
```

### 2. Executar espelhamento

```bash
# Básico
pg-mirror mirror --config config.json

# Com opções adicionais
pg-mirror mirror -c config.json --jobs 8 --drop-existing

# Modo verbose (debug)
pg-mirror -v mirror --config config.json
```

### 3. Validar configuração antes de executar

```bash
pg-mirror validate --config config.json
```

## 📖 Opções do CLI

### Comando `check`

Verifica se as ferramentas PostgreSQL estão instaladas.

```bash
pg-mirror check
```

**Saída de exemplo:**
```
============================================================
System Information:
============================================================
OS: Linux 5.15.0
Platform: Linux-5.15.0-x86_64
Machine: x86_64

============================================================
PostgreSQL Client Tools:
============================================================
✓ pg_dump      : pg_dump (PostgreSQL) 14.5
  Path: /usr/bin/pg_dump
✓ pg_restore   : pg_restore (PostgreSQL) 14.5
  Path: /usr/bin/pg_restore
✓ psql         : psql (PostgreSQL) 14.5
  Path: /usr/bin/psql

============================================================
✓ All system requirements met!
============================================================
```

### Comando `mirror`

| Opção | Descrição |
|-------|-----------|
| `-c, --config PATH` | Caminho para arquivo de configuração (padrão: config.json) |
| `-j, --jobs INTEGER` | Número de jobs paralelos (sobrescreve config) |
| `--drop-existing` | Recriar banco se já existir (sobrescreve config) |
| `--skip-checks` | Pular verificação de ferramentas PostgreSQL |
| `-v, --verbose` | Modo verbose (mostra mensagens DEBUG) |

**Nota:** Por padrão, o comando `mirror` verifica automaticamente se as ferramentas PostgreSQL estão instaladas antes de executar. Use `--skip-checks` para pular esta verificação.

### Comando `validate`

| Opção | Descrição |
|-------|-----------|
| `-c, --config PATH` | Caminho para arquivo de configuração para validar |

## 🎯 Exemplos de Uso

### Migração Produção → Staging

```bash
pg-mirror mirror -c examples/config.prod-to-staging.json --drop-existing
```

### Backup Local com Mais Jobs

```bash
pg-mirror mirror -c config.json --jobs 8
```

### Validar Antes de Executar

```bash
# Validar primeiro
pg-mirror validate -c config.json

# Se OK, executar
pg-mirror mirror -c config.json
```

### Modo Debug

```bash
pg-mirror -v mirror -c config.json
```

## 🔍 Comportamento Inteligente

A ferramenta verifica automaticamente:

1. **Banco não existe**: Cria automaticamente e faz o restore
2. **Banco existe + `drop_existing: false`**: Restaura direto no banco existente
3. **Banco existe + `drop_existing: true`**: Remove e recria o banco antes do restore

## 📊 Logs

Exemplo de saída:

```
2025-11-05 14:32:10 - INFO - ============================================================
2025-11-05 14:32:10 - INFO - Configuração carregada:
2025-11-05 14:32:10 - INFO -    Origem: meu_banco @ origem.exemplo.com
2025-11-05 14:32:10 - INFO -    Destino: meu_banco @ destino.exemplo.com
2025-11-05 14:32:10 - INFO -    Jobs paralelos: 4
2025-11-05 14:32:10 - INFO -    Drop existing: False
2025-11-05 14:32:10 - INFO - ============================================================
2025-11-05 14:32:10 - INFO - Criando backup de 'meu_banco' (origem.exemplo.com)...
2025-11-05 14:32:45 - INFO - Backup criado com sucesso: 245.67 MB
2025-11-05 14:32:45 - INFO - Banco 'meu_banco' não existe. Criando...
2025-11-05 14:32:46 - INFO - Banco 'meu_banco' criado com sucesso
2025-11-05 14:32:46 - INFO - Restaurando em 'meu_banco' (destino.exemplo.com)...
2025-11-05 14:32:46 - INFO - Usando 4 jobs paralelos
2025-11-05 14:35:21 - INFO - Restore concluído com sucesso!
2025-11-05 14:35:21 - INFO - Backup temporário removido
2025-11-05 14:35:21 - INFO - ============================================================
2025-11-05 14:35:21 - INFO - ✅ Espelhamento concluído com sucesso!
2025-11-05 14:35:21 - INFO - ============================================================
```

## 🛠️ Desenvolvimento

### Instalar em modo desenvolvimento

```bash
git clone https://github.com/seu-usuario/pg-mirror.git
cd pg-mirror

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências de desenvolvimento
pip install -r requirements.txt
pip install -e .
```

### Executar testes

```bash
pytest
pytest --cov  # Com cobertura
```

### Estrutura de Módulos

- **cli.py**: Interface CLI com Click
- **backup.py**: Operações de backup com pg_dump
- **restore.py**: Operações de restore com pg_restore
- **database.py**: Gerenciamento de bancos (criar, remover, verificar)
- **config.py**: Carregamento e validação de configuração
- **logger.py**: Setup do sistema de logging
- **system_checks.py**: Verificação de requisitos do sistema

## 📚 Documentação Relacionada

- [Guia Rápido](../guides/QUICKSTART.md)
- [Verificação de Sistema](../guides/SYSTEM_CHECKS.md)
- [Estrutura do Projeto](../project/PROJECT_STRUCTURE.md)
- [Voltar para Documentação](../README.md)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia [CONTRIBUTING.md](../development/CONTRIBUTING.md) para detalhes.

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](../../LICENSE) para detalhes.

## 🐛 Reportar Bugs

Encontrou um bug? Por favor, abra uma [issue](https://github.com/seu-usuario/pg-mirror/issues).

## 📚 Documentação Adicional

- [QUICKSTART.md](QUICKSTART.md) - Guia rápido de início
- [docs/installation.md](docs/installation.md) - Instalação detalhada
- [PUBLISHING_GUIDE.md](PUBLISHING_GUIDE.md) - Guia de publicação
- [examples/](examples/) - Exemplos de configuração

---

⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!
