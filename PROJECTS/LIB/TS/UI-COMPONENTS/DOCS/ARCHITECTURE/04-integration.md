# Integration - @carf/ui

## Integração com GEOWEB/ADMIN

@carf/ui é consumida por GEOWEB e ADMIN via NPM install do GitHub Packages, importando componentes individuais com tree-shaking automático (`import { Button, UnitCard } from '@carf/ui'`). Aplicações consumidoras devem configurar [Tailwind CSS content paths](https://tailwindcss.com/docs/content-configuration) para incluir os paths da lib no `content` do `tailwind.config.js` garantindo que classes Tailwind dos componentes sejam compiladas no bundle final. Theme customization é feita via CSS variables (`--primary`, `--radius`) definidas em `app/globals.css` seguindo [convenções de instalação shadcn/ui](https://ui.shadcn.com/docs/installation), permitindo trocar cores, fontes e espaçamentos sem modificar código dos componentes. Para componentes de domínio (UnitCard, HolderCard), aplicações devem fornecer types de `@carf/tscore` como props e opcionalmente integrar com `@carf/geoapi-client` para data fetching, mantendo lógica de negócio fora da lib de UI.

## Setup em GEOWEB

```json
// package.json
{
  "dependencies": {
    "@carf/ui": "^0.1.0",
    "@carf/tscore": "^0.1.0"
  }
}
```

```ts
// tailwind.config.ts
export default {
  content: [
    "./app/**/*.{ts,tsx}",
    "./node_modules/@carf/ui/**/*.{ts,tsx}"  // Inclui lib
  ]
}
```

```css
/* app/globals.css */
@layer base {
  :root {
    --primary: 220 90% 56%;     /* Azul CARF */
    --radius: 0.5rem;
  }
}
```

```tsx
// app/units/page.tsx
import { UnitCard } from '@carf/ui'
import type { Unit } from '@carf/tscore/types'

export default function UnitsPage() {
  const units: Unit[] = await fetchUnits()

  return (
    <div>
      {units.map(unit => (
        <UnitCard key={unit.id} unit={unit} onEdit={handleEdit} />
      ))}
    </div>
  )
}
```
