---
type: adr
status: approved
updated: 2026-02-07
---

# ADR-003: Expo Router para Navegacao

## Contexto

O REURBCAD precisa de navegacao entre aproximadamente 15 telas com requisitos especificos: grupo de autenticacao isolado do grupo principal, tabs inferiores com visibilidade condicional por role, rotas dinamicas para edicao de entidades por ID, deep linking para callbacks OAuth2 do Keycloak, e tipagem de parametros de rota para evitar erros de navegacao em tempo de execucao.

## Decisao

Expo Router como biblioteca de navegacao, aproveitando o modelo de routing baseado em sistema de arquivos. A estrutura de rotas segue a convencao de diretorios do Expo Router onde cada arquivo dentro da pasta app corresponde a uma rota.

O grupo de autenticacao contem a tela de login. O layout desse grupo verifica se o usuario ja esta autenticado via useAuthStore e redireciona para o grupo principal se sim. Nao exibe tabs nem header.

O grupo principal contem um layout de tabs com tres abas. A aba mapa e a tela padrao exibida apos login para todos os usuarios, servindo como ponto de partida para iniciar cadastros tocando em poligonos. A aba equipe exibe metricas e lista de membros, visivel apenas para usuarios com role field-coordinator. A aba regiao exibe o dashboard com grafico donut de status, tambem visivel apenas para field-coordinator. A visibilidade condicional das tabs e controlada no layout lendo a role do usuario da useAuthStore e ocultando as opcoes de tab via propriedade display none para roles que nao devem ve-las.

Fora do grupo de tabs, existem rotas modais e de detalhe que abrem sobre as tabs sem substitui-las. A tela de unidade recebe o ID como parametro dinamico na rota e exibe todos os dados da unidade com seus titulares e documentos. A tela de novo titular abre como push na stack para preenchimento do formulario. A tela de titular existente recebe o ID do titular para edicao. A tela de assinatura abre em modo landscape forcado para captura de assinatura com o dedo. A tela de scan OCR abre a camera com overlay para captura de documento. A tela de configuracoes exibe opcoes de sincronizacao, preferencias visuais e informacoes do app.

Deep linking configurado com scheme customizado (reurbcad://) para receber callbacks OAuth2 do Keycloak apos autenticacao. O Expo Router trata automaticamente a URL de callback roteando para o handler de autenticacao que extrai o authorization code e completa o fluxo PKCE.

## Justificativa

Expo Router oferece routing baseado em sistema de arquivos eliminando configuracao manual de navegadores e rotas. Deep linking funciona nativamente sem configuracao adicional de linking no React Navigation. Tipagem de rotas e parametros e inferida automaticamente a partir da estrutura de arquivos quando usando TypeScript. Integracao direta com Expo simplifica o setup pois o routing ja vem configurado no template do Expo.

## Alternativas Descartadas

React Navigation puro descartado por exigir configuracao manual de cada navigator (stack, tabs, drawer), definicao explicita de tipos de parametros de rota e configuracao manual de deep linking, resultando em mais codigo de configuracao para o mesmo resultado. React Native Navigation (Wix) descartado por usar navegadores nativos que complicam a integracao com Expo e nao suportam o modelo de filesystem routing.
