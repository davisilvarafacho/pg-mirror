# Exemplos de Uso

Este diretório contém exemplos de arquivos de configuração para diferentes cenários.

## Arquivos Disponíveis

### `config.example.json`
Configuração básica de exemplo. Copie este arquivo para começar:
```bash
cp examples/config.example.json config.json
# Edite config.json com suas credenciais
```

### `config.prod-to-staging.json`
Exemplo de migração de produção para staging, com `drop_existing: true` e 8 jobs paralelos.

### `config.localhost.json`
Exemplo para testar localmente entre duas instâncias PostgreSQL na mesma máquina.

## Como Usar

1. **Escolha um exemplo** que melhor se adequa ao seu caso
2. **Copie o arquivo** para o diretório raiz como `config.json`
3. **Edite as credenciais** (hosts, usuários, senhas)
4. **Execute**:
   ```bash
   pg-mirror mirror --config config.json
   ```

## Dicas

- Use `"drop_existing": false` se quiser preservar dados existentes
- Ajuste `"parallel_jobs"` conforme o poder do seu servidor
- Sempre teste primeiro em ambiente não-produtivo!

## ⚠️ Segurança

**NUNCA** commite arquivos com senhas reais no Git!

Os arquivos de exemplo devem conter apenas placeholders.
