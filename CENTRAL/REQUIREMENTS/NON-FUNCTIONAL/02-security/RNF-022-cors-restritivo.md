---
id: RNF-022
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-022: CORS Restritivo

## Descricao

GEOAPI deve implementar CORS restritivo permitindo apenas origens autorizadas. Previne que websites maliciosos facam chamadas a API em nome de usuarios autenticados.

## Metricas

- Whitelist: dominios GEOWEB (dev, staging, prod) e capacitor://
- Middleware: ASP.NET Core CORS centralizado
- Cache preflight: Access-Control-Max-Age configurado

## Criterios de Aceitacao

1. Apenas origens explicitamente listadas sao permitidas
2. Access-Control-Allow-Credentials apenas para origens confiaveis
3. Metodos e headers permitidos limitados ao necessario
