# Testing - WEBDOCS

## Testing

Testing inclui **(1) Link validation** com `bun run check-links` usando Python script que verifica todos os links internos e externos reportando quebrados, **(2) Acessibilidade** com `axe-core` via `bun run test-a11y` escaneando páginas geradas e reportando violações WCAG, **(3) Visual regression** com Percy ou Chromatic comparando screenshots antes/depois de mudanças, **(4) Performance** com Lighthouse CI em GitHub Actions validando scores mínimos (Performance >90, Accessibility 100, Best Practices >90, SEO 100), e **(5) Content validation** com vale (prose linter) checando grammar, spelling, style guide compliance.

## Comandos

```bash
# Link validation
bun run check-links

# Accessibility
bun run test-a11y

# Lighthouse
npx lighthouse http://localhost:4321 --view

# Performance budget
lighthouse-ci --config=.lighthouserc.json
```

## Lighthouse CI Config

```json
{
  "ci": {
    "collect": {
      "url": ["http://localhost:4321/"],
      "numberOfRuns": 3
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", {"minScore": 0.9}],
        "categories:accessibility": ["error", {"minScore": 1}],
        "categories:seo": ["error", {"minScore": 1}]
      }
    }
  }
}
```

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Contém code blocks - considerar converter para prosa.
