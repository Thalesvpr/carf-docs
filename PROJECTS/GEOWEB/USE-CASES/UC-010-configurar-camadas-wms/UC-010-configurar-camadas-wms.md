---
id: UC-010
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-24
---

# UC-010: Configurar Camadas WMS/WMTS

> **Contexto no Workflow:** UC de configuracao previa. Camadas WMS/WMTS sao configuradas pelo ADMIN antes do workflow iniciar, para fornecer contexto geografico no mapa. Ver [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/README.md).

## Atores

- Primario: ADMIN
- Secundario: Servidores WMS/WMTS externos

## Pre-condicoes

- Usuario autenticado com permissao de configuracao de geoservicos
- URL de servidor WMS/WMTS disponivel

## Fluxo Principal

1. ADMIN acessa menu Configuracoes > Camadas de Mapa
2. Sistema exibe lista de camadas configuradas
3. ADMIN clica em Adicionar Camada WMS
4. Sistema exibe formulario de configuracao
5. ADMIN preenche nome, tipo e URL do servidor
6. ADMIN clica Testar Conexao
7. Sistema executa GetCapabilities no servidor externo
8. Sistema parseia XML e extrai lista de layers
9. Sistema exibe layers disponiveis para selecao
10. ADMIN seleciona layer desejado
11. ADMIN ajusta opacidade, ordem e visibilidade padrao
12. ADMIN informa atribuicao conforme licenca da fonte
13. ADMIN clica Salvar
14. Sistema valida configuracao
15. Sistema cria registro e exibe confirmacao
16. Frontend carrega camada ao iniciar mapa
17. Sistema renderiza tiles conforme viewport do usuario

## Fluxos Alternativos

- FA-001: Adicionar WMTS (tiles pre-renderizados)
- FA-002: Proxy de WMS (evitar CORS)

## Fluxos de Excecao

- FE-001: GetCapabilities falha
- FE-002: XML invalido
- FE-003: Layer nao encontrado
- FE-004: Erro ao renderizar no frontend

## Pos-condicoes

- Camada WMS/WMTS configurada e disponivel
- Usuarios visualizam contexto geografico no mapa
- Atribuicao exibida conforme licenca
