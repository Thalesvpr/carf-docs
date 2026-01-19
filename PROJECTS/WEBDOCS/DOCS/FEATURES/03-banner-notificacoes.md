# Banner de Notificações

Banner no topo do site exibe avisos importantes como manutenções programadas, alertas de segurança, ou anúncios de novas funcionalidades. Conteúdo editável via Decap CMS permite equipe não-técnica publicar avisos sem deploy.

Configuração em collection banners do CMS define campos title, message, type (info, warning, error, success), startDate, endDate, e dismissible. Tipo determina cor do banner (azul info, amarelo warning, vermelho error, verde success). Datas controlam período de exibição automático.

Componente Banner.astro renderizado no layout base consulta collection de banners ativos filtrando por data atual entre startDate e endDate. Múltiplos banners ativos são empilhados. Banner dismissible salva estado em localStorage para não reexibir após usuário fechar.

Estilo visual usa cores semânticas do design system com ícone apropriado para cada tipo. Botão de fechar aparece apenas em banners dismissible. Texto suporta Markdown básico (bold, italic, links) para formatação simples.

Uso típico inclui aviso de manutenção programada criado dias antes com startDate no momento da manutenção, alerta de indisponibilidade durante incidentes com type error, e anúncio de nova versão com type success e link para changelog.

Fallback para arquivo JSON local permite banners de emergência sem depender do CMS. Arquivo src/config/emergency-banner.json é verificado primeiro e sobrepõe banners do CMS se presente. Útil para comunicar indisponibilidade do próprio CMS.

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
