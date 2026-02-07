---
type: leaf
status: approved
updated: 2026-02-07
---

# REURBCAD - Especificacao de Telas

Spec consolidada das telas do aplicativo mobile com correcoes aplicadas da reuniao de validacao (2026-02-06).

## Informacoes do Projeto

| Campo | Valor |
|-------|-------|
| Plataforma | Android (Mobile 412px + Tablet 744px) |
| Modo | Offline-first com sincronizacao posterior |
| Framework | React Native + Expo |
| Autenticacao | **Keycloak proprio** (NAO Gov.br) |
| OCR suportados | CNH e RG novo padrao (CIN) |

## Correcoes Aplicadas (vs spec original)

| Item | Antes | Depois |
|------|-------|--------|
| Autenticacao | Gov.br SSO | Keycloak proprio |
| Filiacao | Mae obrigatoria + Pai opcional | Campo unico **opcional** |
| Moradia | "Inicio de moradia" MM/AAAA | "Tempo de moradia" declaratorio ("5 anos") |
| Campo "Ha conflito?" | Presente no formulario | **Removido** (observacao cobre) |
| Status Atendimento | Misturado com outros tipos | 3 categorias separadas |
| Sexo | Campo "Sexo" | Renomeado para "Genero" |

---

## Tres Categorias de Status (IMPORTANTE)

### A) Status de Atendimento
Progressao do cadastro durante visita de campo.

| Status | Formulario | Progressao |
|--------|------------|------------|
| Ausente | Minimo (foto fachada + localizacao) | → Presente |
| Nao quis | Apenas observacao | Fim |
| Presente | Completo | → Assinado |
| Assinado | Completo + assinatura | Fim |

### B) Tipo de Ocupante
| Tipo | Elegivel titulo? |
|------|------------------|
| Possuidor | SIM |
| Locatario | NAO |

### C) Tipo de Utilizacao
Residencial, Comercio, Misto, Terreno vazio, Nao habitado

---

## Design Tokens

### Cores

Cores primarias da marca: azul escuro #1E40AF usado em headers, botoes primarios e elementos de destaque, azul medio #3B82F6 usado em links, icones ativos e indicadores de selecao. Cores semanticas: sucesso #22C55E para confirmacoes e status positivo, alerta #EAB308 para avisos e status pendente, erro #EF4444 para erros e acoes destrutivas. Escala de neutras: #F8FAFC para fundo de tela, #F1F5F9 para fundo de cards, #E2E8F0 para bordas e separadores, #94A3B8 para texto secundario, #475569 para texto primario, #0F172A para titulos e texto de alto contraste.

Cores por attendance_status no mapa: PRESENTE usa verde #22C55E, AUSENTE usa amarelo #EAB308, NAO_QUIS usa vermelho #EF4444, ASSINADO usa azul #3B82F6, sem status usa cinza #9CA3AF.

### Tipografia

Fonte principal: Inter em todos os pesos. Regular 400 para texto corrido, Medium 500 para labels e campos de formulario, SemiBold 600 para subtitulos e botoes, Bold 700 para titulos e numeros de destaque. Tamanhos: titulo 24px com line-height 32px, subtitulo 18px com line-height 24px, corpo 16px com line-height 24px, legenda 14px com line-height 20px, micro 12px com line-height 16px para badges e indicadores.

### Espacamento

Base de 4px com escala: 4px para padding interno de badges, 8px para gap entre icone e texto, 12px para padding de campos de input, 16px para padding de cards e margens laterais de tela, 24px para espaco entre secoes, 32px para espaco entre grupos de formulario, 48px para margem superior e inferior de tela.

### Border Radius

Pequeno 4px para badges e chips. Medio 8px para cards e inputs. Grande 12px para modais e bottom sheets. Completo 9999px para botoes pill e avatares circulares.

---

## Telas Principais

### E1 - Splash
- Logo REURBCAD centralizado
- Verifica autenticacao → E5 (Mapa) ou E2 (Login)

### E2 - Login
- Logo + Botao "Entrar"
- Abre fluxo **Keycloak** (nao Gov.br)

### E3a/E3b - Permissoes
Tela de solicitacao de permissoes do sistema operacional exibida na primeira abertura do app apos login. Cada permissao e apresentada em tela dedicada com icone representativo da permissao no centro superior, texto explicando porque a permissao e necessaria para o funcionamento do app e botao de concessao na parte inferior.

Sequencia obrigatoria de solicitacao: localizacao primeiro (obrigatoria, bloqueia avanco para a proxima tela se negada pois o app depende de GPS para geolocalizar unidades), camera segundo (necessaria para fotos de fachada e documentos, permite avanco se negada mas limita funcionalidades de captura), galeria terceiro (necessaria para selecionar fotos existentes).

Fallback quando permissao e negada: tela explicativa com texto descrevendo a funcionalidade que ficara indisponivel e botao "Abrir Configuracoes" que direciona para as configuracoes do sistema operacional onde o usuario pode conceder a permissao manualmente. Para localizacao negada, o app nao avanca e exibe mensagem permanente explicando que GPS e obrigatorio para operacao em campo.

### E4 - Preparar Regiao
Tela de download do pacote de dados para operacao offline. Exibida apos concessao de permissoes, antes de acessar o mapa pela primeira vez. Barra de progresso segmentada em tres etapas sequenciais: "Baixando mapa de tiles" (maior parte do tamanho, tipicamente 60-80 porcento do total), "Baixando poligonos vetoriais" (GeoJSON das unidades e comunidades) e "Baixando dados pre-cadastrados" (metadados de comunidades e unidades existentes).

Indicador de tamanho estimado do download exibido antes de iniciar (por exemplo "Pacote estimado: 127 MB"). Botao "Iniciar Download" para confirmar. Botao "Cancelar" visivel durante todo o download para abortar sem perder dados ja existentes. Barra de progresso com percentual numerico e velocidade estimada.

Em caso de erro durante download: mensagem especifica do problema (sem conexao, timeout, erro de servidor) com botao "Tentar Novamente" que retoma do ponto onde parou quando possivel. Download acontece apenas uma vez: apos completado, dados persistem localmente no WatermelonDB e filesystem. A tela nao e exibida novamente a menos que o usuario force redownload via configuracoes.

### E5 - Mapa (Principal)
Tela principal do app exibindo mapa interativo com ortofoto como base, poligonos vetoriais sobre a ortofoto e marcador GPS do usuario atualizado em tempo real. Zoom levels suportados de 14 (visao geral da comunidade) a 20 (detalhe de lote individual).

Toggle de layers no canto superior direito: botao de camadas abrindo menu com checkboxes para ortofoto (base, sempre visivel por padrao), poligonos vetoriais (contornos das unidades sobre a ortofoto) e marcador GPS do usuario.

Botao flutuante circular azul (#3B82F6) no canto inferior direito com icone de adicionar para iniciar novo cadastro de unidade na posicao atual do GPS.

Toque longo em um poligono abre bottom sheet com detalhes resumidos da unidade: codigo, status, attendance_status e botao "Ver detalhes" que navega para tela E7. Toque curto em poligono seleciona a unidade destacando o contorno com borda azul mais grossa.

Agrupamento de marcadores (clustering) em zoom menor que 16: poligonos proximos sao agrupados em circulo com numero indicando quantidade de unidades. Toque no cluster faz zoom in ate nivel onde unidades individuais sao visiveis.

Cores dos poligonos por attendance_status: PRESENTE preenchimento verde #22C55E com 30 porcento de opacidade e borda solida, AUSENTE preenchimento amarelo #EAB308, NAO_QUIS preenchimento vermelho #EF4444, ASSINADO preenchimento azul #3B82F6, sem status preenchimento cinza #9CA3AF.

Bottom navigation visivel apenas para Coordenador com tres tabs: Mapa (ativo por padrao), Equipe e Regiao. Cadastrador ve apenas o mapa sem bottom navigation.

### E6 - Regiao (Dashboard)
Tela exclusiva do Coordenador exibindo metricas consolidadas da operacao de campo da equipe. Acessivel via tab "Regiao" no bottom navigation.

Grafico donut centralizado no topo mostrando distribuicao de unidades por attendance_status com cores correspondentes ao mapa: PRESENTE verde, AUSENTE amarelo, NAO_QUIS vermelho, ASSINADO azul. Numero total de unidades no centro do donut. Legenda abaixo com contagem por status.

Lista de cadastradores da equipe abaixo do grafico. Cada item mostra: avatar ou iniciais do membro, nome, barra de progresso horizontal mostrando unidades cadastradas versus total atribuido (por exemplo "23/45") e percentual de conclusao. Barra verde quando acima de 70 porcento, amarela entre 40 e 70, vermelha abaixo de 40.

Filtro por periodo no topo da tela com segmented control: "Hoje", "Semana", "Total". Alternar o periodo atualiza tanto o donut quanto a lista de membros.

### E7 - Cadastro da Documentacao
Tela de detalhe da unidade exibindo dados cadastrais, titulares vinculados e documentos anexados. Acessada via toque longo em poligono no mapa ou via listagem.

Secao superior com card resumindo dados da unidade: codigo, endereco formatado, attendance_status com badge colorido e data do ultimo cadastro.

Secao de titulares: lista de holders vinculados com nome, CPF parcialmente mascarado (***.***.XXX-XX mostrando apenas ultimos 5 digitos), tipo de vinculo como badge (PROPRIETARIO em azul, CONJUGE em roxo, MORADOR em cinza) e indicador de titular principal com estrela. Botao "Adicionar Titular" abrindo tela E9.

Secao de documentos: lista de documentos da unidade com icone por tipo de documento (camera para FOTO_FACHADA, documento para RG/CPF/CNH, clip para outros), nome do arquivo, data de upload em formato relativo ("ha 2 horas", "ontem"). Botao "Adicionar" abrindo opcoes "Camera" (abre captura direta) ou "Galeria" (abre seletor de arquivos). Preview de documento acessivel por toque com pinch-to-zoom para imagens. Botao de exclusao (icone lixeira) em cada item com dialogo de confirmacao "Tem certeza? Esta acao nao pode ser desfeita." com botoes "Cancelar" e "Excluir" em vermelho.

### E8 - Cadastro da Unidade (Formulario)

**Campos:**
| Campo | Tipo | Obrigatorio | Notas |
|-------|------|-------------|-------|
| Status | Select | SIM | Presente/Ausente/Nao quis |
| Numero unidade | Text | SIM | |
| Rua | Text | SIM | |
| Tempo de moradia | Text | SIM | **Declaratorio**: "5 anos", "mais de 20 anos" |
| Condicao ocupacao | Select | SIM | |
| Foto fachada | Camera | Condicional | **Obrigatorio se Ausente** |
| Observacao | Textarea | Condicional | Obrigatorio se Nao quis |

**Removido**: Campo "Ha conflito?" (coberto por observacao)

**Comportamento condicional:**
- Status = Ausente → campos titular desabilitados, foto fachada obrigatoria
- Status = Presente → formulario completo

### E9 - Novo Titular (Formulario)

**ORDEM DOS CAMPOS (CPF PRIMEIRO!):**

| # | Campo | Tipo | Obrigatorio | Notas |
|---|-------|------|-------------|-------|
| 1 | **CPF** | Masked | SIM | **Primeiro! Bloqueia demais ate validar** |
| 2 | Nome Completo | Text | SIM | Min 2 palavras |
| 3 | Nome Social | Text | NAO | Visivel se checkbox ativado |
| 4 | Data nascimento | Date | SIM | DD/MM/AAAA |
| 5 | Genero | Select | SIM | Masculino, Feminino, Nao declarar, Outros |
| 6 | Filiacao | Text | **NAO** | Campo unico, 1 ou 2 nomes, **opcional** |
| 7 | Estado Civil | Select | SIM | Solteiro, Casado, Divorciado, Viuvo, Separado |
| 8 | Uniao Estavel | Select | Condicional | Nao / Reconhecida cartorio / Nao reconhecida |
| 9 | E-mail | Email | NAO | |
| 10 | Profissao | Searchable | SIM | Lista CBO + "Outros" (obriga texto) |
| 11 | Ocupacao | Text | SIM | Substitui "vinculo empregaticio" |

**Condicional Estado Civil:**
- Casado ou Uniao Estavel → dados conjuge obrigatorios (nome + CPF)

### E10 - Assinatura
- Orientacao: **LANDSCAPE obrigatorio**
- Canvas de desenho com dedo
- Salva como PNG criptografado AES-256
- Campo `signature_path` referencia arquivo
- Status so vira "Assinado" com assinatura valida

### E11 - Configuracoes
- Sincronizacao (status, ultima sync, toggle Wi-Fi only)
- Geral (modo escuro, tela ligada, fonte)
- Sobre (versao, ajuda)
- Sair da conta

---

## Fluxo OCR (Telas Novas N1-N8)

### N1 - Selecao do Documento
- Card CNH ou Card RG/CIN
- Link "Preencher manualmente" pula OCR

### N2 - Instrucao Pre-Captura
- Checklist visual (iluminacao, lente, documento em maos)
- Chips: campos extraidos automaticamente

### N3 - Camera com Overlay
- Fullscreen, corner brackets coloridos
- Auto-captura quando enquadrado + estavel + boa luz
- Captura frente → verso

### N4 - Revisao da Foto
- Preview com pinch-to-zoom
- Chips qualidade (nitidez, iluminacao, enquadramento)
- "Usar esta foto" ou "Tirar novamente"

### N5 - Processamento OCR
- Overlay com animacao scan
- 100% on-device, zero rede
- Progress bar pseudo-determinado

### N6 - Formulario Pre-preenchido
- Campos do E9 pre-preenchidos pelo OCR
- Indicadores de confianca (verde/amarelo/vermelho)
- Toggle "Editar todos os campos"
- Badge "Editado" automatico quando campo alterado
- Rastreamento de acuracia: valorOCR vs valorFinal

### N7 - Confirmacao
- Checkmark sucesso
- Card resumo (nome, CPF mascarado)
- Status sync (aguardando/sincronizado)

### N8 - Estados de Erro
- Falha total OCR → opcao preencher manualmente
- Falha parcial → campos faltantes destacados
- Camera indisponivel → abrir configuracoes
- **Principio**: sempre tem "Preencher manualmente" como escape

---

## Diferencas Coordenador vs Cadastrador

| Elemento | Coordenador | Cadastrador |
|----------|------------|-------------|
| Bottom nav tabs | Equipe, Mapa, Regiao | Apenas Mapa |
| Dashboard (E6) | Visivel | Oculto |
| Metricas equipe | Visivel | Oculto |
| Selecao de regiao | Pode escolher | Regiao pre-atribuida |

---

## Modelo de Dados - Assinatura

| Campo | Tipo | Descricao |
|-------|------|-----------|
| signature_path | String? | Caminho PNG criptografado |
| signature_timestamp | DateTime | Momento da captura |
| signature_device_id | String | ID do dispositivo |

---

## Componentes Primitivos

Botao primario: fundo azul #1E40AF, texto branco, border radius medio 8px, altura 48px, padding horizontal 24px, fonte SemiBold 16px. Estado desabilitado com opacidade 50 porcento. Estado de loading com spinner branco substituindo texto.

Botao secundario: fundo transparente, borda azul #3B82F6 com 1px, texto azul, mesmas dimensoes do primario.

Input de texto: altura 48px, borda #E2E8F0, border radius medio 8px, padding horizontal 12px, fonte Regular 16px, placeholder em #94A3B8. Estado de foco com borda azul #3B82F6. Estado de erro com borda vermelha #EF4444 e mensagem de erro em vermelho 12px abaixo. Estado valido com borda verde #22C55E.

Card: fundo #F1F5F9, border radius grande 12px, padding 16px, sombra sutil com offset y 1px e blur 3px em preto 10 porcento de opacidade.

Badge de status: pill com border radius completo 9999px, padding horizontal 8px vertical 4px, fonte micro 12px SemiBold, cor de fundo correspondente ao status com 15 porcento de opacidade e texto na cor solida.
