---
type: leaf
status: review
updated: 2026-01-24
---

# Avatar

Componente de imagem circular para representacao visual de usuarios.

## Props

Prop src aceita URL da imagem do usuario. Prop alt descreve imagem para acessibilidade. Prop fallback aceita string exibida quando imagem falha ou carrega. Prop size aceita sm, default ou lg controlando dimensoes.

## Fallback

Quando src nao fornecido ou imagem falha, exibe fallback. Fallback tipicamente usa iniciais do nome. Fundo colorido gerado deterministicamente do nome. Texto centralizado com contraste adequado.

## Tamanhos

Size sm renderiza 32x32 pontos para listas compactas. Size default renderiza 40x40 pontos para uso geral. Size lg renderiza 64x64 pontos para perfis e destaque. Tamanhos customizados via className width e height.

## Indicador de Status

Prop status aceita online, offline, busy ou away. Indicador circular pequeno posicionado no canto inferior direito. Cores semanticas: verde online, cinza offline, vermelho busy, amarelo away. Posicao ajusta conforme tamanho do avatar.

## Acessibilidade

Alt text descreve pessoa representada. Fallback text lido como alternativa. Indicador de status anunciado via accessibilityLabel. Imagem decorativa em contextos onde nome aparece adjacente.

## Grupo de Avatars

AvatarGroup empilha multiplos avatars com sobreposicao. Prop max limita quantidade visivel. Excedente exibido como contador numerico. Util para exibir participantes de equipe ou comentarios.
