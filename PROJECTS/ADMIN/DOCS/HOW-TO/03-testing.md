# Testing - ADMIN

## Testes E2E

Testes E2E com Playwright em `e2e/` cobrindo fluxos críticos (login como admin, criar tenant, deletar user, visualizar audit logs), rodar com `bun run test:e2e` que abre browser headless executando testes contra app rodando em `http://localhost:5173`, testes devem setup banco em estado conhecido usando fixtures resetando dados antes de cada test, validar RBAC testando que usuário sem role ADMIN não consegue acessar `/admin`, e CI roda testes em GitHub Actions em cada PR validando que mudanças não quebram fluxos administrativos.

## Comandos

```bash
# Rodar testes E2E
bun run test:e2e

# Rodar em modo UI (debug)
bun run test:e2e --ui

# Rodar testes específicos
bun run test:e2e user-management
```

## Exemplo de Teste

```typescript
test('admin can create tenant', async ({ page }) => {
  // Login
  await page.goto('http://localhost:5173')
  await page.fill('[name=username]', 'admin@carf.gov.br')
  await page.fill('[name=password]', 'admin123')
  await page.click('button[type=submit]')

  // Navigate to tenants
  await page.click('text=Tenants')

  // Create tenant
  await page.click('text=New Tenant')
  await page.fill('[name=name]', 'Test Municipality')
  await page.click('button:has-text("Create")')

  // Verify
  await expect(page.locator('text=Test Municipality')).toBeVisible()
})
```

