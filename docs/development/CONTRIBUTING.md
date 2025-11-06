# Contribuindo para pg-mirror

Obrigado por considerar contribuir com este projeto! 🎉

## 📋 Código de Conduta

Este projeto segue um código de conduta. Ao participar, você concorda em manter um ambiente respeitoso e acolhedor.

## 🤔 Como Posso Contribuir?

### Reportando Bugs

Antes de criar um bug report, verifique se o problema já não foi reportado. Ao criar um bug report, inclua:

- **Descrição clara** do problema
- **Passos para reproduzir** o comportamento
- **Comportamento esperado** vs comportamento atual
- **Screenshots** (se aplicável)
- **Ambiente**:
  - Versão do Python (`python --version`)
  - Versão do PostgreSQL (`psql --version`)
  - Sistema operacional
  - Conteúdo do `config.json` (sem senhas!)
  - Logs completos do erro

### Sugerindo Melhorias

Sugestões de melhorias são bem-vindas! Abra uma issue com:

- **Título descritivo**
- **Descrição detalhada** da funcionalidade
- **Motivação**: Por que isso seria útil?
- **Exemplos**: Como seria usado?

### Pull Requests

1. **Fork** o repositório
2. **Clone** seu fork:
   ```bash
   git clone https://github.com/seu-usuario/pg-mirror.git
   cd pg-mirror
   ```

3. **Crie uma branch** para sua feature:
   ```bash
   git checkout -b feature/minha-feature
   ```

4. **Faça suas alterações** seguindo o guia de estilo

5. **Teste suas mudanças**:
   ```bash
   python -m pytest tests/
   pylint src/
   ```

6. **Commit suas alterações**:
   ```bash
   git add .
   git commit -m "feat: adiciona funcionalidade X"
   ```

7. **Push para sua branch**:
   ```bash
   git push origin feature/minha-feature
   ```

8. **Abra um Pull Request** na branch `main`

## 📝 Guia de Estilo

### Python

- Siga [PEP 8](https://peps.python.org/pep-0008/)
- Use type hints quando possível
- Docstrings em todas as funções públicas
- Máximo de 100 caracteres por linha

Exemplo:

```python
def exemplo_funcao(parametro: str, opcional: int = 10) -> bool:
    """
    Breve descrição da função.
    
    Args:
        parametro: Descrição do parâmetro
        opcional: Descrição do parâmetro opcional
        
    Returns:
        bool: Descrição do retorno
        
    Raises:
        ValueError: Quando parametro é inválido
    """
    if not parametro:
        raise ValueError("parametro não pode ser vazio")
    return True
```

### Commits

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Alterações na documentação
- `style:` Formatação, ponto e vírgula, etc
- `refactor:` Refatoração de código
- `test:` Adição de testes
- `chore:` Tarefas de manutenção

Exemplos:
```
feat: adiciona suporte a backup incremental
fix: corrige erro ao conectar com PostgreSQL 16
docs: atualiza README com novos exemplos
```

### Testes

- Escreva testes para novas funcionalidades
- Mantenha cobertura acima de 80%
- Use nomes descritivos:

```python
def test_create_backup_with_valid_credentials():
    """Testa criação de backup com credenciais válidas"""
    pass

def test_restore_fails_with_invalid_host():
    """Testa que restore falha com host inválido"""
    pass
```

## 🏗️ Estrutura do Projeto

```
pg-mirror/
├── src/
│   └── pg_mirror/
│       ├── __init__.py
│       ├── backup.py          # Lógica de backup
│       ├── restore.py         # Lógica de restore
│       └── config.py          # Gerenciamento de config
├── tests/
│   ├── test_backup.py
│   ├── test_restore.py
│   └── test_config.py
├── docs/
│   ├── installation.md
│   └── configuration.md
├── examples/
│   └── config.example.json
├── db-restore.py              # CLI principal
├── requirements.txt
├── setup.py
└── README.md
```

## 🧪 Testando Localmente

### Setup inicial

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt
```

### Executar testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src/pg_mirror --cov-report=html

# Testes específicos
pytest tests/test_backup.py -v
```

### Linting

```bash
# Verificar código
pylint src/

# Formatação automática
black src/ tests/
isort src/ tests/
```

## 📚 Recursos Úteis

- [Documentação PostgreSQL](https://www.postgresql.org/docs/)
- [Python Testing with pytest](https://docs.pytest.org/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)

## 🎯 Áreas que Precisam de Ajuda

Estamos buscando contribuições especialmente em:

- [ ] Testes unitários e de integração
- [ ] Documentação e exemplos
- [ ] Suporte a outras plataformas
- [ ] Melhorias de performance
- [ ] Tradução do README

## 💬 Dúvidas?

Sinta-se à vontade para:
- Abrir uma [Discussion](https://github.com/seu-usuario/pg-mirror/discussions)
- Entrar em contato via [email]

## � Documentação Relacionada

- [Estrutura do Projeto](../project/PROJECT_STRUCTURE.md)
- [Guia de Publicação](PUBLISHING_GUIDE.md)
- [README Principal](../../README.md)
- [Voltar para Documentação](../README.md)

## �🙏 Reconhecimento

Todos os contribuidores serão adicionados ao README. Obrigado por tornar este projeto melhor!
