# Instalação

## Requisitos do Sistema

### PostgreSQL Client Tools

O projeto requer as ferramentas de linha de comando do PostgreSQL instaladas no sistema:
- `pg_dump`
- `pg_restore`
- `psql`

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install postgresql-client
```

#### Fedora/RHEL/CentOS

```bash
sudo dnf install postgresql
```

#### macOS

```bash
brew install postgresql
```

#### Windows

1. Baixe o instalador em: https://www.postgresql.org/download/windows/
2. Durante a instalação, selecione "Command Line Tools"
3. Adicione ao PATH: `C:\Program Files\PostgreSQL\XX\bin`

### Python

Python 3.8 ou superior é necessário.

Verifique sua versão:
```bash
python --version
```

## Instalação do Projeto

### Opção 1: Instalação como Pacote Python (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/pg-mirror.git
cd pg-mirror

# Instale o pacote
pip install -e .
```

Após a instalação, você pode usar a CLI:
```bash
pg-mirror mirror --config config.json
pg-mirror validate --config config.json
pg-mirror version
```

### Opção 2: Uso Direto (Script Executável)

Se você quer usar sem instalar como pacote:

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/pg-mirror.git
cd pg-mirror

# Instale as dependências
pip install -r requirements.txt

# Execute diretamente via script
./pg-mirror mirror --config config.json
```

### Opção 3: Via PyPI (quando publicado)

```bash
pip install pg-mirror
```

## Instalação para Desenvolvimento

Se você quer contribuir com o projeto:

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/pg-mirror.git
cd pg-mirror

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instale em modo de desenvolvimento com dependências extras
pip install -e ".[dev]"
```

## Verificando a Instalação

### Verificar PostgreSQL tools

```bash
pg_dump --version
pg_restore --version
psql --version
```

Você deve ver algo como:
```
pg_dump (PostgreSQL) 14.5
```

### Verificar Python

```bash
python --version
```

Deve retornar Python 3.8 ou superior.

### Testar o script

```bash
python db-restore.py --help
```

Deve exibir a ajuda do comando.

## Problemas Comuns

### Erro: "pg_dump: command not found"

**Solução**: As ferramentas PostgreSQL não estão instaladas ou não estão no PATH.

1. Instale conforme instruções acima
2. No Windows, adicione ao PATH: Painel de Controle → Sistema → Variáveis de Ambiente

### Erro: "ModuleNotFoundError"

**Solução**: Python não está configurado corretamente.

```bash
# Certifique-se de estar no diretório correto
cd pg-mirror

# Reinstale
pip install -e .
```

### Erro de permissão no PostgreSQL

**Solução**: Verifique as permissões do usuário no banco.

O usuário precisa de:
- `SELECT` no banco de origem (para backup)
- `CREATE DATABASE` no servidor de destino (para restore)

```sql
-- Conceder permissões
GRANT ALL PRIVILEGES ON DATABASE meu_banco TO meu_usuario;
```

## Próximos Passos

Após a instalação, veja:
- [README.md](../README.md) - Documentação principal
- [examples/](../examples/) - Exemplos de configuração
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Guia de contribuição
