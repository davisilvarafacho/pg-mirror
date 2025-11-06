# ⚙️ Configuração GitHub Actions - Guia Rápido

## 📦 O Que Foi Criado

Dois workflows foram implementados:

1. **`.github/workflows/tests.yml`** - Testes automatizados
2. **`.github/workflows/publish.yml`** - Publicação no PyPI

## 🚀 Setup Rápido (5 minutos)

### 1. Commit dos Workflows

```bash
git add .github/
git commit -m "ci: add GitHub Actions workflows for tests and PyPI publishing"
git push origin main
```

### 2. Configurar PyPI (Método Recomendado - Trusted Publishing)

#### No PyPI (https://pypi.org):

1. Crie conta se não tiver
2. Acesse: **Account Settings → Publishing → Add a new pending publisher**
3. Preencha:
   - **PyPI Project Name**: `pg-mirror`
   - **Owner**: seu-usuario-github
   - **Repository name**: pg-mirror
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`
4. Clique em **Add**

#### No GitHub (https://github.com/seu-usuario/pg-mirror):

1. Acesse: **Settings → Environments**
2. Clique em **New environment**
3. Nome: `pypi`
4. (Opcional) Configure proteções:
   - ✅ Required reviewers (você mesmo)
   - ✅ Wait timer: 5 minutos
   - ✅ Deployment branches: `main` only

### 3. Primeiro Teste

```bash
# Fazer uma mudança qualquer
echo "# Test" >> README.md
git add README.md
git commit -m "test: trigger CI"
git push origin main

# Acompanhe em: https://github.com/seu-usuario/pg-mirror/actions
```

## 🧪 Workflow de Testes

### O Que Testa

✅ **15 combinações de ambientes**:
- Ubuntu + Python 3.8, 3.9, 3.10, 3.11, 3.12
- macOS + Python 3.8, 3.9, 3.10, 3.11, 3.12
- Windows + Python 3.8, 3.9, 3.10, 3.11, 3.12

✅ **Verificações adicionais**:
- Linting com ruff
- Formatação com black
- Type checking com mypy
- Cobertura de código com Codecov

### Quando Executa

- ✅ Push em `main` ou `develop`
- ✅ Pull Requests para `main` ou `develop`

### Badge para README

Adicione ao README.md:

```markdown
[![Tests](https://github.com/seu-usuario/pg-mirror/actions/workflows/tests.yml/badge.svg)](https://github.com/seu-usuario/pg-mirror/actions/workflows/tests.yml)
```

## 📦 Workflow de Publicação

### Modo 1: Automático (Recomendado)

Toda vez que você fizer push na `main` com uma nova versão:

```bash
# 1. Atualize a versão
poetry version patch  # 0.1.0 → 0.1.1

# 2. Commit e push
git add pyproject.toml
git commit -m "chore: bump version to $(poetry version -s)"
git push origin main

# 3. GitHub Actions automaticamente:
#    ✅ Executa todos os testes
#    ✅ Publica no PyPI
#    ✅ Cria GitHub Release
```

### Modo 2: Manual (Para controle total)

No GitHub:

1. Acesse: **Actions → Publish to PyPI**
2. Clique em **Run workflow**
3. Selecione tipo de bump:
   - `patch`: correções (0.1.0 → 0.1.1)
   - `minor`: novas funcionalidades (0.1.0 → 0.2.0)
   - `major`: breaking changes (0.1.0 → 1.0.0)
4. Clique em **Run workflow**

O workflow automaticamente:
- ✅ Incrementa a versão
- ✅ Faz commit da mudança
- ✅ Executa testes
- ✅ Publica no PyPI
- ✅ Cria GitHub Release

### Quando Executa

- ✅ Push na `main` com versão alterada
- ✅ Manualmente via Actions UI
- ❌ **NÃO** executa para mudanças apenas em:
  - `docs/**`
  - `**.md`
  - `.gitignore`
  - `examples/**`

## 🔐 Segurança

### Trusted Publishing (Recomendado)

✅ **Vantagens**:
- Sem tokens/senhas no GitHub
- Mais seguro
- Recomendado pelo PyPI

✅ **Já configurado** nos workflows

### Alternativa: Token API (Menos seguro)

Se preferir usar token:

1. **No PyPI**: Gere um API token
2. **No GitHub**: Settings → Secrets → Actions
3. Adicione secret: `PYPI_API_TOKEN`
4. Modifique `.github/workflows/publish.yml`:

```yaml
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    password: ${{ secrets.PYPI_API_TOKEN }}  # Adicione esta linha
```

## 📊 Monitoramento

### Ver Status dos Workflows

```bash
# Via web
https://github.com/seu-usuario/pg-mirror/actions

# Via CLI (gh)
gh run list
gh run view --log
```

### Codecov (Cobertura)

Após primeiro push:

1. Acesse: https://codecov.io/gh/seu-usuario/pg-mirror
2. Autorize GitHub App
3. Badge será gerado automaticamente

Adicione ao README:

```markdown
[![codecov](https://codecov.io/gh/seu-usuario/pg-mirror/branch/main/graph/badge.svg)](https://codecov.io/gh/seu-usuario/pg-mirror)
```

## 🎯 Fluxo de Trabalho Recomendado

### Para Features/Fixes

```bash
# 1. Crie branch
git checkout -b feature/nova-funcionalidade

# 2. Desenvolva e teste localmente
pytest tests/
poetry run pg-mirror check

# 3. Commit
git add .
git commit -m "feat: adiciona nova funcionalidade"

# 4. Push
git push origin feature/nova-funcionalidade

# 5. Abra Pull Request
# GitHub Actions executará testes automaticamente
```

### Para Release

```bash
# Opção A: Bump manual
poetry version minor
git add pyproject.toml
git commit -m "chore: bump version to $(poetry version -s)"
git push origin main
# Publicação automática!

# Opção B: Workflow manual
# GitHub → Actions → Publish to PyPI → Run workflow
```

## ⚠️ Troubleshooting

### Erro: "Trusted publishing exchange failure"

**Solução**: Configure trusted publishing no PyPI (veja passo 2 acima)

### Erro: "Coverage below 50% threshold"

**Solução**:
```bash
# Adicione mais testes
pytest tests/ --cov=pg_mirror --cov-report=html
# Verifique htmlcov/index.html para ver o que falta
```

### Erro: "Version already exists on PyPI"

**Solução**:
```bash
# Bump a versão
poetry version patch
git add pyproject.toml
git commit -m "chore: bump version"
git push
```

### Testes Passam Localmente mas Falham no CI

**Solução**:
```bash
# Teste em múltiplas versões Python
poetry env use 3.8
pytest tests/

poetry env use 3.12
pytest tests/

# Verifique diferenças de SO
# Testes no CI incluem Ubuntu, macOS e Windows
```

## 📝 Checklist de Setup Completo

- [ ] Workflows commitados (`.github/workflows/`)
- [ ] Trusted Publishing configurado no PyPI
- [ ] Environment `pypi` criado no GitHub
- [ ] Primeiro push feito para testar CI
- [ ] Badge de testes adicionado ao README
- [ ] Codecov configurado (opcional)
- [ ] CHANGELOG.md criado
- [ ] Versão inicial definida em `pyproject.toml`

## 🎉 Pronto!

Após o setup, você terá:

✅ Testes automáticos em **15 ambientes diferentes**  
✅ Publicação automática no PyPI  
✅ Releases automáticos no GitHub  
✅ Badges de status  
✅ Relatórios de cobertura  
✅ Linting automático  

**Tudo automatizado e pronto para produção!** 🚀

---

## 📚 Mais Informações

- Documentação completa: [`docs/development/GITHUB_ACTIONS.md`](./GITHUB_ACTIONS.md)
- Guia de publicação: [`docs/development/PUBLISHING_GUIDE.md`](./PUBLISHING_GUIDE.md)
- CHANGELOG: [`CHANGELOG.md`](../../CHANGELOG.md)

---

**Última atualização**: 2025-11-05
