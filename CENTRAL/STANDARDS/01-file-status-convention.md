---
status: rejected
updated: 2026-01-20
---

# Convenção de Status de Arquivo

Todo arquivo markdown em CENTRAL e PROJECTS deve incluir metadados no frontmatter YAML indicando seu estado atual de completude.

## Frontmatter Obrigatório

Todo arquivo `.md` deve começar com um bloco YAML frontmatter contendo os campos obrigatórios. O campo `status` indica o estado atual do documento. O campo `updated` indica a data da última modificação no formato `YYYY-MM-DD`.

```yaml
---
status: rejected
updated: 2026-01-20
---
```

## Campos

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `status` | string | Sim | Estado do documento: `review`, `approved`, `rejected` |
| `updated` | date | Sim | Data da última modificação em `YYYY-MM-DD` |
| `description` | string | Não | Motivo da rejeição (apenas quando `status: rejected`) |

O campo `description` é o **motivo de rejeição**. Ele só deve estar presente quando o status é `rejected`. Quando o documento é aprovado ou volta para review, o campo é automaticamente removido.

## Valores de Status

O status `approved` indica que o arquivo está completo, revisado por humano e aprovado, podendo ser considerado fonte confiável de informação.

O status `review` indica que o arquivo foi gerado ou corrigido automaticamente e aguarda revisão humana para aprovação final. Este é o valor padrão para novos arquivos.

O status `rejected` indica que o arquivo possui problemas estruturais, viola convenções ou precisa de refatoração significativa.

## Exemplos

Arquivo aprovado (sem description):

```yaml
---
status: rejected
updated: 2026-01-20
---
```

Arquivo aguardando revisão (sem description):

```yaml
---
status: rejected
updated: 2026-01-20
---
```

Arquivo rejeitado (com motivo da rejeição):

```yaml
---
status: rejected
updated: 2026-01-20
description: "Incompleto. Standards devem ter regras claras e validaveis, nao apenas diretrizes vagas."
---
```

## Regras

Todos os arquivos `.md` devem ter frontmatter, incluindo READMEs. Se não houver status definido, o padrão é `review`. Se não houver data, usa-se a data atual. Documentos com mais de 6 meses sem atualização são considerados desatualizados e devem ser revisados.

## Validação

O script `normalize_yaml.py` em `.scripts/` normaliza automaticamente o frontmatter de todos os arquivos. O plugin Obsidian Docs Toolkit valida a presença dos metadados obrigatórios e permite aprovar ou rejeitar documentos rapidamente.

```bash
# Verificar o que seria modificado
python .scripts/normalize_yaml.py --dry-run

# Aplicar normalização
python .scripts/normalize_yaml.py
```

## Metadados de ADR

Architecture Decision Records possuem metadados adicionais específicos. O campo `adr_date` indica quando a decisão foi tomada. O campo `adr_status` indica o estado da decisão com valores como `proposed`, `accepted`, `deprecated` ou `superseded`. O campo `deciders` indica quem tomou a decisão.

```yaml
---
status: rejected
updated: 2026-01-20
adr_date: 2026-01-15
adr_status: accepted
deciders: "Equipe de Arquitetura"
---
```
