# RUNBOOKS

Runbooks de troubleshooting do CARF para resolução rápida de incidentes operacionais.

## Problemas Frequentes

- Connection pool exhausted
- JWT expired
- RLS policy block
- Slow queries

## Guia de Troubleshooting

1. Reproduzir o issue
2. Coletar logs com correlation ID
3. Verificar métricas no Grafana
4. Usar distributed tracing para rastrear
5. Testar componentes isoladamente
6. Aplicar fix
7. Validar correção

## Post-mortem

Após resolução, documentar:
- Root cause identificado
- Correção permanente implementada
- Ações para prevenir recorrência

---

**Última atualização:** 2026-01-14
