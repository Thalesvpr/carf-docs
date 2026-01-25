---
type: workflow
status: approved
updated: 2026-01-25
category: regras
---

# Regras de Segregacao por TENANT

Regras que garantem o isolamento de dados entre diferentes regioes/areas de atuacao.

## Regras

| Regra | Descricao |
|-------|-----------|
| TENANT-01 | TENANT e a unidade de segregacao de TUDO no sistema |
| TENANT-02 | Ortofotos sao segregadas por TENANT |
| TENANT-03 | Poligonos sao segregados por TENANT |
| TENANT-04 | Tarefas sao segregadas por TENANT |
| TENANT-05 | Agentes sao segregados por TENANT |
| TENANT-06 | Um usuario SO enxerga e opera dados do(s) TENANT(s) designado(s) |

## Detalhamento

### TENANT-01: Unidade de Segregacao

TENANT e o conceito central de isolamento. Representa uma regiao ou area de atuacao (municipio, assentamento, projeto).

### TENANT-02 a TENANT-05: Segregacao de Recursos

Todos os recursos do sistema sao segregados:
- **Ortofotos**: Armazenadas em pastas separadas no bucket
- **Poligonos**: Comunidades, quadras e lotes pertencem a um TENANT
- **Tarefas**: Trabalhos e atribuicoes sao por TENANT
- **Agentes**: Usuarios sao designados a TENANTs especificos

### TENANT-06: Visibilidade Restrita

Um usuario so consegue:
- Ver dados do(s) TENANT(s) ao qual foi designado
- Operar (criar/editar/excluir) dentro do(s) TENANT(s) designado(s)
- Isolamento garantido via RLS (Row-Level Security) no PostgreSQL
