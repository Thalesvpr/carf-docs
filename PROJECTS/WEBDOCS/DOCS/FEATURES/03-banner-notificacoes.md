---
status: review
updated: 2026-01-21
---

# Banner de Notificações

Banner no topo do site exibe avisos importantes como manutenções programadas, alertas de segurança, ou anúncios de novas funcionalidades. Conteúdo editável via Decap CMS permite equipe não-técnica publicar avisos sem deploy.

Configuração em collection banners do CMS define campos title, message, type (info, warning, error, success), startDate, endDate, e dismissible. Tipo determina cor do banner (azul info, amarelo warning, vermelho error, verde success). Datas controlam período de exibição automático.

Componente Banner.astro renderizado no layout base consulta collection de banners ativos filtrando por data atual entre startDate e endDate. Múltiplos banners ativos são empilhados. Banner dismissible salva estado em localStorage para não reexibir após usuário fechar.

Estilo visual usa cores semânticas do design system com ícone apropriado para cada tipo. Botão de fechar aparece apenas em banners dismissible. Texto suporta Markdown básico (bold, italic, links) para formatação simples.

Uso típico inclui aviso de manutenção programada criado dias antes com startDate no momento da manutenção, alerta de indisponibilidade durante incidentes com type error, e anúncio de nova versão com type success e link para changelog.

Fallback para arquivo JSON local permite banners de emergência sem depender do CMS. Arquivo src/config/emergency-banner.json é verificado primeiro e sobrepõe banners do CMS se presente. Útil para comunicar indisponibilidade do próprio CMS.

## Componente Banner.astro

```astro
---
// src/components/Banner.astro
import { getCollection } from 'astro:content';

interface Banner {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'warning' | 'error' | 'success';
  dismissible: boolean;
  startDate: Date;
  endDate: Date;
}

// Verifica banner de emergência primeiro
let emergencyBanner: Banner | null = null;
try {
  const emergency = await import('../config/emergency-banner.json');
  if (emergency.active) {
    emergencyBanner = emergency as Banner;
  }
} catch {
  // Arquivo não existe, continua normalmente
}

// Busca banners do CMS
const now = new Date();
const allBanners = await getCollection('banners');
const activeBanners = allBanners
  .filter(b => new Date(b.data.startDate) <= now && new Date(b.data.endDate) >= now)
  .map(b => ({ id: b.id, ...b.data }));

// Emergência tem prioridade
const banners = emergencyBanner ? [emergencyBanner] : activeBanners;

const typeStyles = {
  info: { bg: 'bg-blue-50 dark:bg-blue-900/30', border: 'border-blue-200', text: 'text-blue-800 dark:text-blue-200', icon: 'ℹ️' },
  warning: { bg: 'bg-yellow-50 dark:bg-yellow-900/30', border: 'border-yellow-200', text: 'text-yellow-800 dark:text-yellow-200', icon: '⚠️' },
  error: { bg: 'bg-red-50 dark:bg-red-900/30', border: 'border-red-200', text: 'text-red-800 dark:text-red-200', icon: '🚨' },
  success: { bg: 'bg-green-50 dark:bg-green-900/30', border: 'border-green-200', text: 'text-green-800 dark:text-green-200', icon: '✅' }
};
---

{banners.map((banner) => {
  const style = typeStyles[banner.type];
  return (
    <div
      class={`banner ${style.bg} ${style.border} ${style.text} border-b px-4 py-3`}
      data-banner-id={banner.id}
      data-dismissible={banner.dismissible}
    >
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span class="text-xl">{style.icon}</span>
          <div>
            <strong class="font-semibold">{banner.title}</strong>
            <p class="text-sm" set:html={banner.message} />
          </div>
        </div>
        {banner.dismissible && (
          <button
            class="banner-dismiss p-1 hover:opacity-70"
            aria-label="Fechar"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  );
})}

<script>
  // Verifica banners dismissíveis
  document.querySelectorAll('.banner[data-dismissible="true"]').forEach(banner => {
    const id = banner.getAttribute('data-banner-id');
    const dismissedKey = `banner-dismissed-${id}`;

    // Esconde se já foi fechado
    if (localStorage.getItem(dismissedKey)) {
      banner.remove();
      return;
    }

    // Handler de fechamento
    banner.querySelector('.banner-dismiss')?.addEventListener('click', () => {
      localStorage.setItem(dismissedKey, 'true');
      banner.remove();
    });
  });
</script>
```

## Collection Schema (banners)

```typescript
// src/content/config.ts (adicionar à config existente)
import { z, defineCollection } from 'astro:content';

const bannersCollection = defineCollection({
  type: 'data',
  schema: z.object({
    title: z.string().max(100),
    message: z.string().max(500),
    type: z.enum(['info', 'warning', 'error', 'success']),
    dismissible: z.boolean().default(true),
    startDate: z.coerce.date(),
    endDate: z.coerce.date(),
    active: z.boolean().default(true)
  })
});

export const collections = {
  // ... outras collections
  banners: bannersCollection
};
```

## Arquivo de Exemplo do Banner

```json
// src/content/banners/manutencao-2024-01.json
{
  "title": "Manutenção Programada",
  "message": "O sistema ficará indisponível das 02:00 às 04:00 do dia 25/01 para atualização. <a href='/changelog'>Saiba mais</a>",
  "type": "warning",
  "dismissible": true,
  "startDate": "2024-01-24T00:00:00Z",
  "endDate": "2024-01-25T04:00:00Z",
  "active": true
}
```

## Decap CMS Collection Config

```yaml
# public/admin/config.yml (adicionar)
collections:
  - name: "banners"
    label: "Banners de Notificação"
    folder: "src/content/banners"
    create: true
    extension: "json"
    format: "json"
    fields:
      - { label: "Título", name: "title", widget: "string", hint: "Máximo 100 caracteres" }
      - { label: "Mensagem", name: "message", widget: "text", hint: "Suporta HTML básico para links" }
      - { label: "Tipo", name: "type", widget: "select", options: ["info", "warning", "error", "success"] }
      - { label: "Pode fechar?", name: "dismissible", widget: "boolean", default: true }
      - { label: "Data início", name: "startDate", widget: "datetime" }
      - { label: "Data fim", name: "endDate", widget: "datetime" }
      - { label: "Ativo", name: "active", widget: "boolean", default: true }
```

## Banner de Emergência (sem CMS)

```json
// src/config/emergency-banner.json
{
  "id": "emergency",
  "title": "Sistema Indisponível",
  "message": "Estamos trabalhando para restaurar o serviço. Acompanhe em <a href='https://status.carf.com.br'>status.carf.com.br</a>",
  "type": "error",
  "dismissible": false,
  "startDate": "2024-01-20T00:00:00Z",
  "endDate": "2024-12-31T23:59:59Z",
  "active": true
}
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
