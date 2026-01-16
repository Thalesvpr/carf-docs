# Unit Management Feature

Documentação da feature de gerenciamento de unidades habitacionais.

## Visão Geral

A feature de gerenciamento de unidades permite cadastrar, visualizar, editar e aprovar unidades habitacionais dentro do sistema CARF, incluindo:

- Cadastro com endereço e geometria georreferenciada
- Upload de fotos da unidade
- Vinculação de titulares
- Workflow de aprovação
- Visualização em mapa

## User Stories

### US-001: Cadastrar Unidade

```gherkin
Como cadastrista
Quero cadastrar uma nova unidade habitacional
Para iniciar o processo de regularização fundiária

Critérios de Aceitação:
- Deve informar endereço completo
- Deve desenhar polígono no mapa ou informar coordenadas
- Área é calculada automaticamente
- Código único é gerado (UNI-YYYY-NNNNN)
- Status inicial é "Rascunho"
```

### US-002: Visualizar Unidades no Mapa

```gherkin
Como usuário do sistema
Quero visualizar unidades no mapa
Para entender a distribuição geográfica

Critérios de Aceitação:
- Exibir polígonos das unidades com cores por status
- Clustering em zoom baixo
- Popup com informações resumidas ao clicar
- Filtros por status, bairro, comunidade
```

### US-003: Submeter para Análise

```gherkin
Como cadastrista
Quero submeter unidade para análise
Para que aprovador possa avaliar

Critérios de Aceitação:
- Só permite se houver pelo menos um titular vinculado
- Status muda de "Rascunho" para "Pendente"
- Notifica aprovadores do tenant
- Registra histórico com timestamp e usuário
```

## Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | /api/units | Criar unidade |
| GET | /api/units/{id} | Obter unidade |
| GET | /api/units | Listar com filtros |
| PATCH | /api/units/{id} | Atualizar |
| DELETE | /api/units/{id} | Excluir (rascunho) |
| POST | /api/units/{id}/submit | Submeter para análise |
| POST | /api/units/{id}/approve | Aprovar |
| POST | /api/units/{id}/reject | Rejeitar |
| GET | /api/units/geojson | Export GeoJSON |

## Regras de Negócio

1. **RN-001**: Geometria deve ser polígono válido (fechado, sem auto-intersecção)
2. **RN-002**: Geometria não pode sobrepor unidade existente no mesmo tenant
3. **RN-003**: Área mínima 10m², máxima 100.000m²
4. **RN-004**: Coordenadas devem estar dentro do município do tenant
5. **RN-005**: Unidades aprovadas não podem ser editadas
6. **RN-006**: Exclusão só permitida em status "Rascunho"

## Diagrama de Estados

```
[Rascunho] --submit--> [Pendente] --approve--> [Aprovado]
                              |
                              +--reject--> [Rejeitado]
```

## Permissões

| Ação | cadastrista | analista | aprovador | admin |
|------|-------------|----------|-----------|-------|
| Criar | ✓ | ✓ | ✓ | ✓ |
| Editar | ✓ | ✓ | ✓ | ✓ |
| Visualizar | ✓ | ✓ | ✓ | ✓ |
| Submeter | ✓ | ✓ | ✓ | ✓ |
| Aprovar | | | ✓ | ✓ |
| Rejeitar | | | ✓ | ✓ |
| Excluir | ✓ | ✓ | ✓ | ✓ |

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
