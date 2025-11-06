# 🚀 Guia de Publicação - Open Source

Este documento descreve o processo completo para publicar o projeto como open source.

## 📋 Checklist Pré-Publicação

### Código
- [ ] Código revisado e limpo
- [ ] Comentários e docstrings completos
- [ ] Remover credenciais/senhas hardcoded
- [ ] Testes funcionando
- [ ] Sem TODOs críticos

### Documentação
- [x] README.md completo
- [x] LICENSE escolhida
- [x] CONTRIBUTING.md
- [x] CHANGELOG.md
- [ ] Screenshots/GIFs (se aplicável)

### Configuração
- [x] .gitignore apropriado
- [x] pyproject.toml configurado
- [x] requirements.txt
- [x] Exemplos de configuração

## 🔧 Passo 1: Preparar o Repositório Git

```bash
# Inicializar Git (se ainda não foi feito)
cd /home/rafacho/Área\ de\ trabalho/prod-debug
git init

# Adicionar todos os arquivos
git add .

# Primeiro commit
git commit -m "feat: initial commit - PostgreSQL backup/restore tool

- Backup paralelo com pg_dump
- Restore multi-threaded
- Verificação inteligente de banco
- Logging estruturado
- Configuração via JSON"

# Criar branch main
git branch -M main
```

## 🌐 Passo 2: Criar Repositório no GitHub

### Via Interface Web:

1. Acesse https://github.com/new
2. Preencha:
   - **Nome**: `pg-mirror` (ou `postgresql-backup-restore`)
   - **Descrição**: "Ferramenta performática para backup e restore de PostgreSQL com processamento paralelo"
   - **Público** ✅
   - **Não** inicialize com README (já temos)
3. Clique em "Create repository"

### Conectar o Repositório Local:

```bash
# Substitua 'seu-usuario' pelo seu username do GitHub
git remote add origin https://github.com/seu-usuario/pg-mirror.git

# Push inicial
git push -u origin main
```

## 🏷️ Passo 3: Criar Primeira Release

### 3.1 Criar Tag

```bash
# Tag da versão 1.0.0
git tag -a v1.0.0 -m "Release v1.0.0

Recursos iniciais:
- Backup paralelo com formato custom
- Restore multi-threaded (até 4 jobs)
- Verificação inteligente de existência do banco
- Sistema de logging estruturado
- Configuração via JSON
- Suporte a drop_existing"

# Push da tag
git push origin v1.0.0
```

### 3.2 Criar Release no GitHub

1. Acesse: `https://github.com/seu-usuario/pg-mirror/releases/new`
2. Escolha a tag: `v1.0.0`
3. Título: `v1.0.0 - Initial Release`
4. Descrição (use o CHANGELOG.md como base):

```markdown
## 🎉 Primeira Release!

Ferramenta performática para backup e restore de bancos PostgreSQL entre servidores.

### ✨ Recursos

- 🚀 Backup paralelo com formato custom do PostgreSQL
- ⚡ Restore multi-threaded com até 4 jobs paralelos
- 🔍 Verificação inteligente de existência do banco
- 📝 Sistema de logging estruturado
- ⚙️ Configuração via arquivo JSON
- 🛡️ Gerenciamento seguro de conexões e arquivos temporários

### 📦 Instalação

```bash
git clone https://github.com/seu-usuario/pg-mirror.git
cd pg-mirror
pip install -r requirements.txt
```

### 🚀 Uso Rápido

```bash
# Copie o exemplo de configuração
cp examples/config.example.json config.json

# Edite com suas credenciais
nano config.json

# Execute
python db-restore.py --config config.json
```

### 📖 Documentação

Veja o [README.md](https://github.com/seu-usuario/pg-mirror#readme) para documentação completa.

### 🐛 Reportar Bugs

Encontrou um problema? [Abra uma issue](https://github.com/seu-usuario/pg-mirror/issues/new)!
```

5. Clique em "Publish release"

## 📦 Passo 4: Publicar no PyPI (Opcional)

### 4.1 Preparação

```bash
# Instalar ferramentas
pip install build twine

# Build do pacote
python -m build
```

Isso criará:
- `dist/pg_mirror-1.0.0.tar.gz`
- `dist/pg_mirror-1.0.0-py3-none-any.whl`

### 4.2 Testar no Test PyPI

```bash
# Criar conta em https://test.pypi.org
# Criar API token

# Upload para Test PyPI
twine upload --repository testpypi dist/*

# Testar instalação
pip install --index-url https://test.pypi.org/simple/ pg-mirror
```

### 4.3 Publicar no PyPI Real

```bash
# Criar conta em https://pypi.org
# Criar API token

# Upload para PyPI
twine upload dist/*

# Testar
pip install pg-mirror
```

## 🔄 Passo 5: Configurar CI/CD (Opcional mas Recomendado)

Crie `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov pylint
    
    - name: Lint with pylint
      run: |
        pylint db-restore.py --disable=C0103,C0114
      continue-on-error: true
    
    - name: Test with pytest
      run: |
        pytest tests/ -v --cov
```

## 🎨 Passo 6: Adicionar Badges ao README

Edite o `README.md` e adicione no topo:

```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub release](https://img.shields.io/github/release/seu-usuario/pg-mirror.svg)](https://github.com/seu-usuario/pg-mirror/releases)
[![Tests](https://github.com/seu-usuario/pg-mirror/workflows/Tests/badge.svg)](https://github.com/seu-usuario/pg-mirror/actions)
```

## 📢 Passo 7: Divulgação

### Reddit
- r/Python - "Show and Tell"
- r/PostgreSQL
- r/devops
- r/selfhosted

### Dev.to
Escreva um artigo:
```
Título: "Criando uma Ferramenta Open Source para Backup PostgreSQL"
Tags: python, postgresql, opensource, devops
```

### Twitter/LinkedIn
```
🎉 Acabei de publicar minha primeira ferramenta open source!

pg-mirror: Ferramenta performática para backup/restore de PostgreSQL

✨ Backup paralelo
⚡ Restore multi-threaded
🔍 Verificação inteligente de bancos

Confira: https://github.com/seu-usuario/pg-mirror

#Python #PostgreSQL #OpenSource
```

### Hacker News
- Título: "Show HN: pg-mirror - PostgreSQL Database Mirroring Tool with Parallel Processing"
- URL: Link do GitHub

## 🔧 Manutenção Contínua

### Responder Issues
- Meta: Responder em até 48 horas
- Use labels: `bug`, `enhancement`, `question`, `good first issue`

### Aceitar Pull Requests
1. Review cuidadoso do código
2. Verificar testes
3. Atualizar CHANGELOG.md
4. Fazer merge e agradecer!

### Criar Releases Regulares
Quando tiver mudanças significativas:
```bash
# Atualizar versão em pyproject.toml
# Atualizar CHANGELOG.md

git add .
git commit -m "chore: bump version to 1.1.0"
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin main --tags

# Criar release no GitHub
```

## 📊 Monitorar Métricas

Acompanhe:
- ⭐ Stars no GitHub
- 🍴 Forks
- 👀 Watchers
- 📥 Downloads do PyPI
- 🐛 Issues abertas/fechadas
- 🔀 Pull Requests

## 🎯 Objetivos de Curto Prazo

- [ ] 10 stars no GitHub
- [ ] 5 contribuidores
- [ ] Cobertura de testes > 80%
- [ ] Documentação completa
- [ ] 100 downloads no PyPI

## 🎉 Parabéns!

Seu projeto está oficialmente open source! 🚀

Lembre-se:
- **Seja paciente**: Crescimento leva tempo
- **Seja gentil**: Agradeça contribuições
- **Seja consistente**: Mantenha o projeto ativo
- **Divirta-se**: Open source é sobre comunidade!

---

Dúvidas? Abra uma issue ou consulte:
- https://opensource.guide/
- https://docs.github.com/en/repositories
