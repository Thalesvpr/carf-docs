---
id: UC-001-FA-001
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-001-FA-001: Desenhar Geometria Offline (Mobile)

Fluxo alternativo do UC-001 para captura de geometria via GPS no app mobile quando offline.

## Condicao

No passo 5 do UC-001, usuario FIELD_AGENT esta no app mobile sem conexao de rede.

## Fluxo

1. Usuario seleciona opcao Capturar com GPS
2. Sistema ativa geolocalizacao do dispositivo
3. Usuario caminha pelo perimetro da unidade
4. Sistema coleta pontos GPS automaticamente a cada 3-5 metros
5. Sistema exibe trilha em tempo real no mapa offline
6. Usuario pode ajustar vertices manualmente arrastando no mapa
7. Usuario pressiona Concluir Poligono
8. Sistema fecha poligono e valida (minimo 3 pontos, sem auto-intersecoes)
9. Sistema calcula area e salva geometria localmente com flag pendente

## Retorno

Volta ao passo 6 do UC-001 com geometria salva localmente aguardando sincronizacao.

## Pos-condicoes

- Geometria salva no banco local com needs_sync=true
- Badge laranja indica pendencia de sincronizacao
- Sincronizacao automatica quando conexao retornar
