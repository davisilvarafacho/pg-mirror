# 🧪 Testes Unitários do pg-mirror

Este diretório contém os testes unitários completos para o projeto pg-mirror.

## 📋 Estrutura de Testes

```
tests/
├── conftest.py              # Fixtures compartilhadas e configuração pytest
├── test_backup.py           # Testes para pg_mirror.backup
├── test_config.py           # Testes para pg_mirror.config
├── test_database.py         # Testes para pg_mirror.database
├── test_logger.py           # Testes para pg_mirror.logger
├── test_restore.py          # Testes para pg_mirror.restore
└── test_system_checks.py    # Testes para pg_mirror.system_checks
```

## ✅ Cobertura de Testes

### Módulos Testados

| Módulo | Arquivo de Teste | Funções/Classes | Cobertura |
|--------|------------------|-----------------|-----------|
| `backup.py` | `test_backup.py` | `create_backup`, `cleanup_backup` | ✅ Completo |
| `config.py` | `test_config.py` | `load_config` | ✅ Completo |
| `database.py` | `test_database.py` | `check_database_exists`, `create_database`, `drop_and_create_database` | ✅ Completo |
| `logger.py` | `test_logger.py` | `setup_logger` | ✅ Completo |
| `restore.py` | `test_restore.py` | `restore_backup` | ✅ Completo |
| `system_checks.py` | `test_system_checks.py` | Todas as funções + `SystemCheckError` | ✅ Completo |

### Funcionalidades Testadas

#### 🔧 test_backup.py (12 testes)
- ✅ Criação bem-sucedida de backup
- ✅ Estrutura correta do comando pg_dump
- ✅ Definição de PGPASSWORD no ambiente
- ✅ Cleanup em caso de falha
- ✅ Cálculo de tamanho do arquivo
- ✅ Remoção de arquivo temporário
- ✅ Tratamento de erros durante cleanup
- ✅ Comportamento com filepath None/vazio

#### ⚙️ test_config.py (10 testes)
- ✅ Carregamento de configuração válida
- ✅ Aplicação de valores padrão
- ✅ Erro quando arquivo não existe
- ✅ Erro com JSON inválido
- ✅ Validação de seções obrigatórias (source, target)
- ✅ Validação de campos obrigatórios
- ✅ Configuração com portas customizadas
- ✅ Configuração com opções customizadas

#### 🗄️ test_database.py (10 testes)
- ✅ Verificação de banco existente
- ✅ Verificação de banco inexistente
- ✅ Estrutura correta dos comandos psql
- ✅ Criação de banco bem-sucedida
- ✅ Tratamento de erro na criação
- ✅ Drop e create de banco
- ✅ Terminação de conexões antes do drop
- ✅ Tratamento de exceções

#### 📝 test_logger.py (12 testes)
- ✅ Criação do logger
- ✅ Nível INFO por padrão
- ✅ Nível DEBUG com verbose=True
- ✅ Presença de handlers
- ✅ Tipo de handler (StreamHandler)
- ✅ Configuração do formatter
- ✅ Remoção de handlers existentes
- ✅ Mensagens INFO, DEBUG, WARNING, ERROR
- ✅ Comportamento com/sem verbose

#### 🔄 test_restore.py (8 testes)
- ✅ Restore bem-sucedido
- ✅ Estrutura correta do comando pg_restore
- ✅ Restore com avisos (sucesso)
- ✅ Restore com erros (falha)
- ✅ Definição de PGPASSWORD
- ✅ Uso de jobs paralelos
- ✅ Logging de informações

#### 🔍 test_system_checks.py (21 testes)
- ✅ Obtenção de informações do SO
- ✅ Verificação de comando existente/inexistente
- ✅ Obtenção de versão de comando
- ✅ Verificação de todas as ferramentas PostgreSQL
- ✅ Detecção de ferramentas faltantes
- ✅ Instruções de instalação por SO (Linux, macOS, Windows)
- ✅ Verificação completa de requisitos do sistema
- ✅ Levantamento de erro quando ferramenta falta
- ✅ Verificação de versão Python
- ✅ SystemCheckError exception

## 🚀 Como Executar os Testes

### Executar Todos os Testes

```bash
pytest
```

### Executar com Cobertura

```bash
pytest --cov=pg_mirror --cov-report=html
```

### Executar Testes de um Módulo Específico

```bash
# Testes de backup
pytest tests/test_backup.py

# Testes de config
pytest tests/test_config.py

# Testes de system checks
pytest tests/test_system_checks.py
```

### Executar em Modo Verbose

```bash
pytest -v
```

### Executar com Saída Detalhada

```bash
pytest -vv
```

### Executar um Teste Específico

```bash
pytest tests/test_config.py::TestLoadConfig::test_load_valid_config
```

## 📊 Relatório de Cobertura

Para gerar relatório de cobertura HTML:

```bash
pytest --cov=pg_mirror --cov-report=html
```

Depois abra `htmlcov/index.html` no navegador.

## 🔧 Fixtures Disponíveis

### Em `conftest.py`

| Fixture | Descrição |
|---------|-----------|
| `mock_logger` | Mock do logger para testes |
| `valid_config` | Configuração completa válida |
| `minimal_config` | Configuração mínima válida |
| `temp_config_file` | Arquivo temporário de configuração |
| `temp_backup_file` | Arquivo temporário de backup |
| `mock_subprocess_success` | Mock de subprocess bem-sucedido |
| `mock_subprocess_error` | Mock de subprocess com erro |
| `mock_os_info_linux` | Mock de info do OS Linux |
| `mock_os_info_darwin` | Mock de info do OS macOS |
| `mock_os_info_windows` | Mock de info do OS Windows |

## 🎯 Estratégia de Testes

### Mocking
- **subprocess.run**: Mockado para evitar execução real de comandos PostgreSQL
- **tempfile**: Mockado para controlar criação de arquivos temporários
- **os.path/os.unlink**: Mockado para evitar operações de arquivo reais
- **platform**: Mockado para testar diferentes sistemas operacionais

### Casos de Teste
1. **Casos de Sucesso**: Fluxos normais funcionando corretamente
2. **Casos de Erro**: Comportamento quando falhas ocorrem
3. **Casos de Borda**: Valores None, vazios, formatos inesperados
4. **Validação**: Estrutura de comandos e argumentos corretos

## 📈 Estatísticas

- **Total de Arquivos de Teste**: 6
- **Total de Classes de Teste**: 19
- **Total de Testes**: 73+
- **Cobertura Esperada**: >90%

## 🐛 Debugging de Testes

### Ver Saída de Print

```bash
pytest -s
```

### Parar no Primeiro Erro

```bash
pytest -x
```

### Ver Traceback Completo

```bash
pytest --tb=long
```

### Executar Testes que Falharam

```bash
pytest --lf
```

## 💡 Boas Práticas

1. **Sempre execute os testes antes de commit**
2. **Mantenha cobertura acima de 80%**
3. **Use fixtures para código duplicado**
4. **Mocke operações externas (IO, subprocess, network)**
5. **Teste casos de sucesso E falha**
6. **Teste valores de borda e edge cases**
7. **Mantenha testes independentes entre si**

## 🔗 Recursos

- [Documentação pytest](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

**Última atualização:** 5 de novembro de 2025  
**Versão:** pg-mirror v1.0.0
