---
id: UC-004
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-004: Coletar Dados em Campo (Mobile)

## Atores

- Primario: FIELD_AGENT
- Secundario: Sistema de GPS, Camera do dispositivo

## Pre-condicoes

- App mobile instalado e autenticado
- Dados da comunidade alvo sincronizados previamente
- GPS habilitado no dispositivo

## Fluxo Principal

1. FIELD_AGENT chega na localizacao da unidade
2. App detecta modo offline e exibe indicador visual
3. FIELD_AGENT clica em Nova Unidade
4. Sistema abre formulario otimizado para mobile
5. Sistema captura localizacao GPS automaticamente
6. FIELD_AGENT preenche dados basicos (endereco, tipo, moradores)
7. FIELD_AGENT desenha geometria (caminhar perimetro ou desenho manual)
8. Sistema valida geometria e calcula area
9. FIELD_AGENT tira fotos da unidade
10. FIELD_AGENT cadastra titulares moradores
11. FIELD_AGENT clica Salvar
12. Sistema valida dados localmente
13. Sistema salva no banco local com status Pending Approval
14. Sistema exibe confirmacao e contador de pendencias

## Fluxos Alternativos

- FA-001: Sincronizar imediatamente
- FA-002: Voice-to-text
- FA-003: Copiar unidade anterior

## Fluxos de Excecao

- FE-001: GPS nao disponivel
- FE-002: Memoria cheia
- FE-003: Bateria baixa

## Pos-condicoes

- Unidade salva localmente com status Pending Approval
- Fotos armazenadas no dispositivo
- Flag needs_sync ativo para sincronizacao posterior
