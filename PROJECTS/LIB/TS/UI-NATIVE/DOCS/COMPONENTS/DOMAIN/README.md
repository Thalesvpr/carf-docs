---
type: readme
status: review
updated: 2026-01-24
---

# Componentes de Dominio

Componentes especificos do ecossistema CARF que integram com tipos do @carf/tscore.

O componente [StatusBadge](./01-status-badge.md) renderiza badge colorido baseado em UnitStatus ou LegitimationStatus. Cores semanticas comunicam estado do workflow visualmente.

O componente [UnitCard](./02-unit-card.md) exibe resumo de unidade habitacional com codigo, endereco e status. Recebe objeto Unit tipado e formata dados automaticamente.

O componente [HolderCard](./03-holder-card.md) exibe dados de titular com nome, CPF formatado e contato. Recebe objeto Holder tipado e usa value objects de validacao.

O componente [CommunityCard](./04-community-card.md) exibe resumo de comunidade com nome, tipo e contagem de unidades. Variantes compact e expanded para listas e detalhes.

O componente [MapComponent](./05-map-component.md) wrapper de react-native-maps com layers, clustering e draw mode para demarcacao de unidades. Integra com ortofoto tiles e WatermelonDB.

O componente [CameraOverlay](./06-camera-overlay.md) camera com guias visuais para captura de documentos, faces e fachadas. Usa expo-camera com modos de overlay configuravel.

O componente [SignatureCanvas](./07-signature-canvas.md) canvas para assinatura digital via toque com captura de path e exportacao PNG base64. Inclui metadados de timestamp e deviceId.

<!-- CARF-INDEX-START -->
<!-- CARF-INDEX-END -->
