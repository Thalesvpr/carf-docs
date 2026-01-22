---
type: leaf
status: review
updated: 2026-01-21
---

# Troubleshooting - Runtime

Resolução de problemas de runtime, performance e desenvolvimento local.

Arquivos relacionados:
- Problemas de auth: `09-troubleshooting-auth.md`
- Problemas de build: `09-troubleshooting-build.md`

## Problemas de Status Page

### Health Check Sempre Failing

**Sintoma:** Serviço mostra como offline mesmo estando online.

```json
{
  "problem": "health_check_failing",
  "debug_steps": [
    {
      "step": 1,
      "action": "Testar endpoint diretamente",
      "command": "curl -v https://api.carf.com.br/health"
    },
    {
      "step": 2,
      "action": "Verificar timeout",
      "check": "Timeout configurado pode ser muito curto"
    },
    {
      "step": 3,
      "action": "Verificar CORS",
      "check": "Health endpoint deve permitir origem do WEBDOCS"
    },
    {
      "step": 4,
      "action": "Verificar SSL",
      "check": "Certificado válido e não expirado"
    }
  ]
}
```

### Status Page Mostra Dados Antigos

**Sintoma:** Status não atualiza mesmo com refresh.

```json
{
  "problem": "stale_status",
  "cause": "SSR com cache ou CDN cache",
  "solutions": [
    "Verificar Cache-Control: no-cache no response",
    "Adicionar ?t={timestamp} na URL",
    "Verificar vercel.json não está cacheando /status"
  ]
}
```

## Problemas de Performance

### Página Carrega Lentamente

**Sintoma:** Lighthouse mostra score baixo de performance.

```json
{
  "problem": "slow_page_load",
  "diagnostic": {
    "tool": "Lighthouse ou WebPageTest",
    "metrics": ["LCP", "FCP", "TTI", "CLS"]
  },
  "common_fixes": {
    "large_images": {
      "issue": "Imagens não otimizadas",
      "fix": "Usar astro:assets para otimização automática"
    },
    "blocking_scripts": {
      "issue": "JS bloqueando render",
      "fix": "Adicionar defer ou async em scripts"
    },
    "unused_css": {
      "issue": "CSS não utilizado",
      "fix": "PurgeCSS ou revisar imports"
    },
    "no_caching": {
      "issue": "Assets sem cache headers",
      "fix": "Configurar Cache-Control conforme SPECS/24"
    }
  }
}
```

## Problemas de Desenvolvimento Local

### Bun/Node Version Mismatch

**Sintoma:** Erros estranhos ou comportamento inconsistente.

```json
{
  "problem": "version_mismatch",
  "check": {
    "bun": "bun --version (esperado: >= 1.0.0)",
    "node": "node --version (esperado: >= 20.0.0)"
  },
  "fix": {
    "bun": "curl -fsSL https://bun.sh/install | bash",
    "node": "nvm use 20"
  }
}
```

### Hot Reload Não Funciona

**Sintoma:** Mudanças no código não refletem no browser.

```json
{
  "problem": "hot_reload_broken",
  "solutions": [
    "Verificar se dev server está rodando",
    "Reiniciar dev server (Ctrl+C e bun dev)",
    "Limpar cache do Astro: rm -rf .astro",
    "Verificar se arquivo está sendo watched"
  ]
}
```

### Erro de Permissão em Windows

**Sintoma:** `EPERM: operation not permitted`.

```json
{
  "problem": "windows_permission",
  "solutions": [
    "Fechar VSCode/editores que podem estar lockando arquivos",
    "Executar terminal como administrador",
    "Desabilitar antivírus temporariamente",
    "Usar WSL2 para desenvolvimento"
  ]
}
```

## Logs e Debugging

### Habilitar Debug Logs

```bash
# Astro verbose
DEBUG=astro:* bun dev

# Apenas auth
DEBUG=auth:* bun dev

# Tudo
DEBUG=* bun dev
```

### Verificar Logs em Produção (Vercel)

```bash
# Via CLI
vercel logs https://docs.carf.com.br --follow

# Ou via dashboard
# Vercel > Project > Deployments > Functions > Logs
```

## Checklist de Diagnóstico

```json
{
  "diagnostic_checklist": [
    "[ ] Console do browser sem erros?",
    "[ ] Network tab mostra requests OK (200)?",
    "[ ] Cookies estão sendo salvos?",
    "[ ] Variáveis de ambiente configuradas?",
    "[ ] Build local passa sem erros?",
    "[ ] Keycloak está acessível?",
    "[ ] GeoAPI health check OK?",
    "[ ] DNS resolvendo corretamente?",
    "[ ] SSL/TLS válido?"
  ]
}
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
