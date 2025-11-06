# 🚀 Guia Rápido de Início

Este guia vai te ajudar a começar em 5 minutos!

## ⚡ Setup Rápido

### 1. Instale as ferramentas PostgreSQL

```bash
# Ubuntu/Debian
sudo apt-get install postgresql-client

# macOS
brew install postgresql

# Verifique
pg_dump --version
```

### 2. Configure suas credenciais

```bash
# Copie o exemplo
cp examples/config.example.json config.json

# Edite com suas credenciais
nano config.json  # ou use seu editor favorito
```

**Exemplo mínimo**:
```json
{
  "source": {
    "host": "servidor-origem.com",
    "database": "meu_banco",
    "user": "postgres",
    "password": "senha123"
  },
  "target": {
    "host": "servidor-destino.com",
    "user": "postgres",
    "password": "senha456"
  }
}
```

### 3. Execute!

```bash
pg-mirror mirror --config config.json
```

## 🎯 Cenários Comuns

### Copiar banco entre servidores

```json
{
  "source": {"host": "prod.db", "database": "app", ...},
  "target": {"host": "staging.db", ...},
  "options": {"drop_existing": true}
}
```

### Backup local

```json
{
  "source": {"host": "remoto.db", "database": "app", ...},
  "target": {"host": "localhost", ...},
  "options": {"parallel_jobs": 2}
}
```

### Refresh de desenvolvimento

```json
{
  "source": {"host": "prod.db", ...},
  "target": {"host": "localhost", ...},
  "options": {
    "drop_existing": true,
    "parallel_jobs": 4
  }
}
```

## 📊 Entendendo os Logs

Você verá mensagens como:

```
2025-11-05 14:32:10 - INFO - Criando backup de 'meu_banco'...
2025-11-05 14:32:45 - INFO - Backup criado com sucesso: 245.67 MB
2025-11-05 14:32:45 - INFO - Banco 'meu_banco' não existe. Criando...
2025-11-05 14:35:21 - INFO - Migração concluída com sucesso!
```

## ⚙️ Opções Importantes

### `drop_existing`

- **`false`** (padrão): Mantém o banco se existir
- **`true`**: Remove e recria o banco (⚠️ cuidado!)

### `parallel_jobs`

- **2-4**: Máquinas normais
- **4-8**: Servidores potentes
- **8+**: Servidores muito potentes

## 🆘 Problemas Comuns

### ❌ Erro: "pg_dump: command not found"

**Solução**: Instale PostgreSQL client tools (veja passo 1)

### ❌ Erro: "permission denied"

**Solução**: Verifique se o usuário tem permissões:
- Origem: precisa de `SELECT` no banco
- Destino: precisa de `CREATE DATABASE`

### ❌ Erro: "could not connect"

**Solução**: Verifique:
- Host e porta corretos
- Firewall permite conexão
- PostgreSQL aceita conexões remotas

### ❌ Erro: "database exists"

**Solução**: Use `"drop_existing": true` se quiser sobrescrever

## 📚 Mais Informações

- [README.md](README.md) - Documentação completa
- [examples/](examples/) - Mais exemplos
- [docs/installation.md](docs/installation.md) - Instalação detalhada

## 💡 Dicas Pro

1. **Teste primeiro**: Sempre teste em ambiente não-produtivo
2. **Backup de segurança**: Faça backup antes de usar `drop_existing: true`
3. **Performance**: Mais `parallel_jobs` = mais rápido (mas usa mais recursos)
4. **Segurança**: Nunca commite `config.json` com senhas reais!
5. **Monitoring**: Acompanhe os logs para detectar problemas cedo

---

**Pronto!** 🎉 Você já pode começar a usar o pg-mirror!

## 📚 Próximos Passos

- [Referência Completa da CLI](../reference/README_CLI.md)
- [Verificação de Sistema](SYSTEM_CHECKS.md)
- [Guia de Instalação](../installation.md)
- [Voltar para Documentação](../README.md)

Algum problema? Abra uma [issue](https://github.com/seu-usuario/pg-mirror/issues).
