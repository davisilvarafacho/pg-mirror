# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não Lançado]

### Em Desenvolvimento
- Testes para CLI (cli.py)
- Melhoria de cobertura para system_checks.py

## [1.0.0] - 2025-11-05

### 🎉 Primeiro Release

### Adicionado

#### Core Features
- Backup paralelo com formato custom do PostgreSQL usando `pg_dump`
- Restore multi-threaded com até 8 jobs paralelos usando `pg_restore`
- Verificação inteligente de existência do banco antes do restore
- Suporte a drop e recreação de banco de destino
- Gerenciamento automático de arquivos temporários
- Sistema de logging estruturado com níveis INFO e DEBUG

#### CLI (Command Line Interface)
- Comando `pg-mirror mirror` para executar migração completa
- Comando `pg-mirror check` para verificar ferramentas PostgreSQL
- Opção `--config` para arquivo de configuração JSON
- Opção `--verbose` para logging detalhado
- Opção `--skip-checks` para pular verificações de sistema

#### System Checks
- Detecção automática do sistema operacional
- Verificação de instalação de ferramentas PostgreSQL (pg_dump, pg_restore, psql)
- Detecção de versões das ferramentas
- Instruções de instalação específicas por SO (Linux, macOS, Windows)
- Verificação de versão do Python (≥3.8)

#### Configuração
- Suporte a arquivo JSON de configuração
- Validação completa de campos obrigatórios
- Valores padrão inteligentes (porta: 5432, parallel_jobs: 4)
- Seções `source`, `target` e `options`

#### Testes
- 74 testes unitários implementados com pytest
- 100% de taxa de sucesso (74/74 passando)
- 53% de cobertura de código
- 5 módulos com 100% de cobertura (config, database, logger, restore, __init__)
- Fixtures reutilizáveis em conftest.py
- Suporte a pytest-cov para relatórios de cobertura

#### Documentação
- README completo com exemplos
- Guia de início rápido (QUICKSTART.md)
- Documentação da CLI (README_CLI.md)
- Guia de verificação de sistema (SYSTEM_CHECKS.md)
- Estrutura do projeto (PROJECT_STRUCTURE.md)
- Guia de contribuição (CONTRIBUTING.md)
- Guia de publicação (PUBLISHING_GUIDE.md)
- Documentação dos testes (tests/README.md)
- Documentação do GitHub Actions (GITHUB_ACTIONS.md)
- Organização em subpastas: guides/, reference/, development/, project/

#### CI/CD
- GitHub Actions workflow para testes automatizados
- Matriz de testes (Ubuntu, macOS, Windows × Python 3.8-3.12)
- GitHub Actions workflow para publicação automática no PyPI
- Bump automático de versão com Poetry
- Criação automática de GitHub Releases
- Integração com Codecov para cobertura de código
- Linting com ruff, black e mypy
- Trusted Publishing com PyPI

### Funcionalidades Técnicas
- Suporte a Python 3.8+
- Type hints em todo o código
- Tratamento robusto de erros com exceções customizadas
- Variáveis de ambiente para senhas (PGPASSWORD)
- Processamento paralelo configurável (1-8 jobs)
- Compressão nativa do PostgreSQL
- Limpeza automática de recursos
- Terminação automática de conexões antes de drop
- Segurança: senhas não aparecem em logs ou comandos visíveis

### Dependências
- click ≥8.0 - CLI moderna
- pytest ≥8.4.2 - Framework de testes
- pytest-cov ≥7.0.0 - Cobertura de código
- PostgreSQL client tools (pg_dump, pg_restore, psql)

### Plataformas Suportadas
- ✅ Linux (Ubuntu, Debian, RHEL, CentOS, Fedora, Arch)
- ✅ macOS (via Homebrew)
- ✅ Windows (via instalador oficial ou Chocolatey)

### Casos de Uso
- Migração entre ambientes (Dev → Staging → Prod)
- Clone de bancos para desenvolvimento local
- Backup e restore de bancos PostgreSQL
- Disaster Recovery (DR)
- Refresh de ambientes de homologação

---

## Tipos de Mudanças

- `Added` (Adicionado) - para novas funcionalidades
- `Changed` (Modificado) - para mudanças em funcionalidades existentes
- `Deprecated` (Obsoleto) - para funcionalidades que serão removidas
- `Removed` (Removido) - para funcionalidades removidas
- `Fixed` (Corrigido) - para correções de bugs
- `Security` (Segurança) - para vulnerabilidades corrigidas

---

[1.0.0]: https://github.com/seu-usuario/pg-mirror/releases/tag/v1.0.0
