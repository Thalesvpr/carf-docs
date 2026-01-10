# Troubleshooting - ADMIN

## Problemas Comuns

**(1) 401 Unauthorized ao acessar /admin** - validar que JWT tem role ADMIN ou SUPER_ADMIN, verificar que `VITE_KEYCLOAK_URL` está correto, fazer logout e login novamente, **(2) API calls failing** - checar console do navegador para ver erro detalhado, comum ser CORS se `VITE_API_URL` está incorreto, ou timeout se GEOAPI está lento, **(3) Styles not loading** - garantir que build incluiu Tailwind classes de shadcn/ui, rodar `bun run build` completo, limpar cache do navegador, **(4) Cannot delete tenant** - verificar se tenant tem dependências (unidades, usuários), GEOAPI retorna erro detalhado em response com lista de dependências, **(5) Protected routes not working** - verificar que React Router está configurado corretamente, middleware validando role existe e está sendo executado.

## Soluções

### 401 Error

```bash
# Limpar tokens e refazer login
localStorage.clear()
# Refresh página
# Login novamente
```

### CORS Error

```javascript
// Verificar VITE_API_URL
console.log(import.meta.env.VITE_API_URL)
// Deve apontar para GEOAPI (ex: http://localhost:7001)
```

