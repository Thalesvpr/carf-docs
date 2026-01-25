---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
---

# RF-151: Popup de Feature

## Descricao

Sistema deve exibir popup ou tooltip ao clicar em feature renderizada no mapa, contendo informacoes detalhadas incluindo atributos e opcoes de acao, permitindo acesso rapido a dados e funcionalidades contextuais sem navegar para outra tela. Popup exibido ao clicar em qualquer feature visivel (ponto, linha ou poligono) aparece imediatamente adjacente ao local clicado, permanecendo visivel ate usuario fechar explicitamente ou clicar em outra feature. Conteudo do popup inclui atributos formatados da feature apresentando pares chave-valor das properties customizadas em layout organizado. Popup inclui botoes de acao contextuais para edicao e exclusao quando usuario tem permissoes apropriadas, acionando modais ou modos de edicao inline. Interface do popup e responsiva adaptando tamanho e posicionamento conforme conteudo e espaco disponivel.

## Criterios de Aceitacao

1. Popup ao clicar em feature
2. Exibicao de atributos formatados
3. Botoes de edicao e exclusao contextuais
4. Posicionamento responsivo
5. Fechamento por clique externo

## Rastreabilidade

- Modulos: GEOWEB
- Requisitos dependentes: RF-132, RF-133, RF-134
