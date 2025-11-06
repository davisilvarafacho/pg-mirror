# GitHub Actions Workflows

Este projeto utiliza GitHub Actions para automação de CI/CD. Temos dois workflows principais:

## 🧪 Workflow de Testes (tests.yml)

### Triggers
- Push nas branches `main` e `develop`
- Pull Requests para `main` e `develop`

### Jobs

#### 1. Test Job
**Matriz de Testes:**
- Sistemas Operacionais: Ubuntu, macOS, Windows
- Versões Python: 3.8, 3.9, 3.10, 3.11, 3.12

**O que faz:**
- ✅ Instala ferramentas PostgreSQL client (pg_dump, pg_restore, psql) em cada SO
- ✅ Configura cache de dependências pip
- ✅ Instala dependências com Poetry
- ✅ Executa todos os testes com pytest
- ✅ Gera relatório de cobertura XML
- ✅ Envia cobertura para Codecov

**Total**: 15 execuções (3 SOs × 5 versões Python)

#### 2. Lint Job
**O que faz:**
- ✅ Verifica código com ruff (linter rápido)
- ✅ Verifica formatação com black
- ✅ Verifica tipos com mypy (continua mesmo com erros)

#### 3. Coverage Report Job
**Executa apenas em Pull Requests**

**O que faz:**
- ✅ Gera relatório HTML de cobertura
- ✅ Comenta o PR com estatísticas de cobertura
- ✅ Indicadores visuais:
  - 🟢 Verde: ≥70% cobertura
  - 🟠 Laranja: 50-69% cobertura
  - 🔴 Vermelho: <50% cobertura

### Requisitos
Nenhuma configuração necessária! O workflow é executado automaticamente.

### Badges
Adicione ao README.md:
```markdown
[![Tests](https://github.com/seu-usuario/pg-mirror/actions/workflows/tests.yml/badge.svg)](https://github.com/seu-usuario/pg-mirror/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/seu-usuario/pg-mirror/branch/main/graph/badge.svg)](https://codecov.io/gh/seu-usuario/pg-mirror)
```

---

## 📦 Workflow de Publicação PyPI (publish.yml)

### Triggers

#### 1. Automático (Push na main)
```
git push origin main
```
- Ignora mudanças em: `docs/`, `*.md`, `.gitignore`, `examples/`
- Publica APENAS se a versão no `pyproject.toml` foi alterada

#### 2. Manual (Workflow Dispatch)
Acessar: **Actions → Publish to PyPI → Run workflow**

Opções:
- `patch`: 0.1.0 → 0.1.1 (correções)
- `minor`: 0.1.0 → 0.2.0 (novas funcionalidades)
- `major`: 0.1.0 → 1.0.0 (breaking changes)

### Jobs

#### 1. Check Version
**O que faz:**
- ✅ Extrai versão atual do `pyproject.toml`
- ✅ Compara com commit anterior
- ✅ Decide se deve publicar

#### 2. Test
**O que faz:**
- ✅ Executa suite completa de testes
- ✅ Verifica cobertura mínima de 50%
- ✅ Falha se testes não passarem

#### 3. Bump Version (opcional)
**Executa se:**
- Workflow manual OU
- Push automático sem mudança de versão

**O que faz:**
- ✅ Incrementa versão com Poetry
- ✅ Commita mudança: `chore: bump version to X.Y.Z [skip ci]`
- ✅ Push automático (não dispara novo workflow)

#### 4. Publish
**Executa se:**
- Testes passaram E
- Versão mudou (ou foi bumped)

**O que faz:**
- ✅ Build do pacote com Poetry (wheel + sdist)
- ✅ Publica no PyPI usando trusted publishing
- ✅ Cria GitHub Release automático com:
  - Tag: `vX.Y.Z`
  - Release notes geradas automaticamente
  - Link para PyPI
  - Instruções de instalação
- ✅ (Opcional) Publica em Test PyPI se workflow manual

### Configuração Necessária

#### 1. PyPI Trusted Publishing (Recomendado)

**No PyPI:**
1. Acesse: https://pypi.org/manage/account/publishing/
2. Adicione um novo publisher:
   - **PyPI Project Name**: `pg-mirror`
   - **Owner**: seu-usuario
   - **Repository**: pg-mirror
   - **Workflow**: publish.yml
   - **Environment**: pypi

**No GitHub:**
1. Acesse: Settings → Environments
2. Crie environment chamado `pypi`
3. (Opcional) Adicione proteções:
   - Required reviewers
   - Wait timer
   - Deployment branches: `main` only

#### 2. Alternativa: PyPI Token (Menos seguro)

**No PyPI:**
1. Acesse: Account Settings → API tokens
2. Crie token com escopo para `pg-mirror`

**No GitHub:**
1. Acesse: Settings → Secrets → Actions
2. Adicione secret: `PYPI_API_TOKEN`

**Modifique publish.yml:**
```yaml
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    password: ${{ secrets.PYPI_API_TOKEN }}  # Adicione esta linha
    verbose: true
```

### Fluxo de Publicação

#### Cenário 1: Publicação Automática
```bash
# 1. Atualize a versão
poetry version patch  # ou minor, major

# 2. Commit e push
git add pyproject.toml
git commit -m "chore: bump version to 0.1.1"
git push origin main

# 3. GitHub Actions automaticamente:
#    - Executa testes
#    - Publica no PyPI
#    - Cria GitHub Release
```

#### Cenário 2: Publicação Manual
```bash
# 1. Push seu código (sem mudar versão)
git push origin main

# 2. No GitHub:
#    Actions → Publish to PyPI → Run workflow
#    Selecione: patch/minor/major
#    Click: Run workflow

# 3. GitHub Actions automaticamente:
#    - Incrementa versão
#    - Commita mudança
#    - Executa testes
#    - Publica no PyPI
#    - Cria GitHub Release
```

#### Cenário 3: Apenas Testes (sem publicar)
```bash
# Push em branch diferente de main
git checkout -b feature/nova-funcionalidade
git push origin feature/nova-funcionalidade

# Ou: push em main mas sem mudanças em código
# (apenas docs, markdown, etc)
```

### Proteções

#### Skip CI
Commits com `[skip ci]` no título não disparam workflows:
```bash
git commit -m "docs: update README [skip ci]"
```

#### Paths Ignore
Mudanças apenas nestes arquivos NÃO disparam publicação:
- `docs/**`
- `**.md`
- `.gitignore`
- `examples/**`

#### Coverage Threshold
Publicação falha se cobertura < 50%

---

## 📋 Boas Práticas

### Versionamento Semântico

Siga [SemVer](https://semver.org/):

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
  ```bash
  poetry version major
  ```

- **MINOR** (0.1.0 → 0.2.0): Novas funcionalidades (compatível)
  ```bash
  poetry version minor
  ```

- **PATCH** (0.1.0 → 0.1.1): Correções de bugs
  ```bash
  poetry version patch
  ```

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat: adiciona suporte a backup incremental
fix: corrige erro no restore paralelo
docs: atualiza documentação de instalação
chore: atualiza dependências
test: adiciona testes para backup.py
refactor: melhora estrutura do módulo config
perf: otimiza processo de restore
```

### Workflow do Desenvolvedor

```bash
# 1. Crie branch para feature/fix
git checkout -b feature/minha-funcionalidade

# 2. Desenvolva e teste localmente
pytest tests/
poetry run pg-mirror check

# 3. Commit e push
git add .
git commit -m "feat: adiciona nova funcionalidade"
git push origin feature/minha-funcionalidade

# 4. Abra Pull Request
# GitHub Actions executará testes automaticamente

# 5. Após aprovação e merge na main
# Decida sobre publicação:

# Opção A: Bump manual antes do merge
poetry version patch
git add pyproject.toml
git commit -m "chore: bump version to 0.1.1"

# Opção B: Deixe GitHub Actions bumpar automaticamente
# Apenas faça merge, depois execute workflow manual
```

---

## 🔍 Troubleshooting

### Testes Falhando no CI mas Passando Localmente

**Problema**: Diferenças de ambiente

**Soluções**:
```bash
# Teste em múltiplas versões Python localmente
poetry env use 3.8
poetry install
pytest tests/

poetry env use 3.12
poetry install
pytest tests/

# Verifique ferramentas PostgreSQL
pg_dump --version
pg_restore --version
psql --version
```

### Publicação Falha: "Project already exists"

**Problema**: Versão já publicada no PyPI

**Soluções**:
```bash
# Verifique versão atual no PyPI
pip index versions pg-mirror

# Bump versão
poetry version patch
git add pyproject.toml
git commit -m "chore: bump version"
git push
```

### Trusted Publishing Não Configurado

**Erro**: `Error: Trusted publishing exchange failure`

**Solução**:
1. Configure trusted publishing no PyPI (veja acima)
2. OU use token API (menos recomendado)

### Coverage Abaixo do Threshold

**Erro**: `Coverage below 50% threshold`

**Solução**:
```bash
# Adicione mais testes
# Verifique cobertura localmente
pytest tests/ --cov=pg_mirror --cov-report=html
# Abra: htmlcov/index.html

# Identifique código não coberto
pytest tests/ --cov=pg_mirror --cov-report=term-missing
```

---

## 📊 Monitoramento

### Acompanhar Execuções
- GitHub: **Actions** tab
- Ver logs detalhados
- Re-executar jobs falhados

### Codecov Dashboard
- https://codecov.io/gh/seu-usuario/pg-mirror
- Visualizar tendências de cobertura
- Cobertura por arquivo/função

### PyPI Releases
- https://pypi.org/project/pg-mirror/
- Estatísticas de downloads
- Versões publicadas

---

## 🚀 Comandos Úteis

```bash
# Ver versão atual
poetry version

# Bump versão
poetry version patch|minor|major

# Build local (sem publicar)
poetry build

# Publicar manualmente (não recomendado)
poetry publish

# Testar instalação do TestPyPI
pip install --index-url https://test.pypi.org/simple/ pg-mirror

# Ver logs do último workflow
gh run list --limit 1
gh run view --log

# Re-executar último workflow
gh run rerun

# Ver workflows disponíveis
gh workflow list

# Disparar workflow manual
gh workflow run publish.yml -f version_bump=patch
```

---

## 📝 Checklist de Setup

- [ ] Repositório no GitHub criado
- [ ] Poetry configurado (`pyproject.toml` completo)
- [ ] Testes passando localmente (`pytest tests/`)
- [ ] Workflows commitados (`.github/workflows/*.yml`)
- [ ] Projeto registrado no PyPI
- [ ] Trusted Publishing configurado no PyPI
- [ ] Environment `pypi` criado no GitHub
- [ ] Badge de testes adicionado ao README
- [ ] Badge de cobertura adicionado ao README (opcional)
- [ ] CHANGELOG.md criado
- [ ] Primeiro release feito

---

**Última atualização**: 2025-11-05  
**Versão**: 1.0
