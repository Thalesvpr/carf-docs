---
type: leaf
status: review
updated: 2026-02-07
---

# SignatureCanvas

Componente de canvas nativo para captura de assinatura digital via toque.

## Props

Prop onSave callback invocado com imagem base64 da assinatura ao confirmar. Prop strokeWidth numero definindo espessura do traco padrao 2. Prop strokeColor cor do traco padrao preto. Prop backgroundColor cor de fundo do canvas padrao branco. Prop clearLabel texto do botao de limpar padrao Limpar. Prop confirmLabel texto do botao de confirmar padrao Confirmar.

## Captura

PanGestureHandler captura coordenadas do toque criando path da assinatura. Path renderiza em tempo real como SVG Path com stroke configurado. Multiplos strokes suportados com interrupcao natural entre tracos. Canvas registra sequencia de pontos para reconstrucao fiel da assinatura.

## Controles

Botao limpar reseta canvas removendo todos strokes capturados. Botao confirmar renderiza canvas como imagem PNG base64 e invoca onSave. Controles posicionados na base do canvas abaixo da area de desenho. Confirmacao desabilita enquanto canvas vazio para prevenir assinatura invalida.

## Metadados

Imagem salva inclui timestamp ISO da captura nos metadados. DeviceId do dispositivo anexado para rastreabilidade da assinatura. Resolucao da imagem padronizada para consistencia entre dispositivos. Hash da imagem gerado para verificacao de integridade.

## Acessibilidade

AccessibilityLabel descreve canvas como area de assinatura digital. AccessibilityHint instrui usuario a desenhar assinatura com dedo. Botoes de limpar e confirmar recebem labels descritivos. Canvas nao acessivel a leitores de tela por natureza visual, botoes compensam.

## Estilizacao

Canvas ocupa largura total do container com aspect ratio 3:1 para proporcao natural. Borda sutil border-input delimita area de desenho. Fundo branco garante contraste com traco preto. Dark mode mantem fundo branco no canvas para impressao adequada.
