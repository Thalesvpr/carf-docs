---
type: leaf
status: review
updated: 2026-02-07
---

# CameraOverlay

Componente de camera nativo com overlay de guias visuais para captura de documentos e fotos.

## Props

Prop mode aceita document, face ou facade definindo tipo de captura com overlay apropriado. Prop onCapture callback invocado com imagem capturada em formato base64. Prop overlayType aceita brackets, circle ou none controlando guia visual exibido. Prop quality numero de 0 a 1 definindo qualidade da imagem capturada.

## Modos de Captura

Modo document exibe brackets retangulares guiando enquadramento de documentos como CPF e RG. Modo face exibe circulo central guiando posicionamento de rosto para foto de titular. Modo facade exibe guia amplo para captura de fachada de unidade habitacional. Cada modo ajusta resolucao e aspect ratio para caso de uso.

## Overlay

Brackets renderizam quatro cantos em L posicionados para enquadrar area de captura. Circle renderiza anel centralizado com area externa escurecida para foco. None remove guias visuais para captura livre sem restricao de enquadramento. Cor dos guias usa branco semi-transparente para visibilidade sobre qualquer fundo.

## Preview

Preview exibe imagem capturada antes de confirmar para revisao do usuario. Botoes de confirmar e repetir disponibilizam decisao sobre qualidade da captura. Preview renderiza em tela cheia com controles sobrepostos na base. Metadados de timestamp e localizacao anexados automaticamente a captura.

## Acessibilidade

AccessibilityLabel descreve modo de captura ativo para leitores de tela. Botao de captura recebe accessibilityRole button com hint descritivo. Flash e alternancia de camera acessiveis via accessibilityActions. Sons de feedback ao capturar complementam indicacao visual.

## Integracao

Usa expo-camera para acesso a camera com permissoes gerenciadas. Imagem salva como PNG base64 para armazenamento e sincronizacao. Compressao automatica baseada em quality prop para economia de armazenamento. Metadados incluem coordenadas GPS quando permissao de localizacao concedida.
