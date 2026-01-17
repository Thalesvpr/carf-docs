# Maintenance Checklist

Checklist para janelas de manutenção programadas do sistema CARF.

## Pré-Manutenção (H-24)

- [ ] Notificar usuários por email sobre janela de manutenção
- [ ] Atualizar status page (status.carf.com.br)
- [ ] Confirmar equipe de plantão disponível
- [ ] Revisar changelog das mudanças a serem aplicadas

## Pré-Manutenção (H-1)

- [ ] Verificar backup mais recente completou com sucesso
- [ ] Executar backup adicional fresh antes da manutenção
```bash
pg_dump -h postgres -U carf -d carf -Fc -Z9 -f pre_maintenance_$(date +%Y%m%d).dump
```
- [ ] Verificar métricas baseline (para comparação pós-manutenção)
- [ ] Preparar scripts de rollback

## Início da Manutenção (H-0)

- [ ] Ativar modo manutenção no load balancer
```bash
kubectl annotate ingress carf-ingress nginx.ingress.kubernetes.io/custom-http-errors="503"
```
- [ ] Verificar que novos requests estão sendo rejeitados (503)
- [ ] Aguardar conexões ativas finalizarem (max 5 min)
- [ ] Escalar deployments para 0 replicas
```bash
kubectl scale deployment geoapi --replicas=0
kubectl scale deployment geoweb --replicas=0
```

## Durante a Manutenção

- [ ] Executar procedimentos planejados
- [ ] Documentar qualquer desvio do plano
- [ ] Verificar logs de erro durante execução
- [ ] Manter comunicação com equipe via Slack #ops-maintenance

## Pós-Manutenção

- [ ] Escalar deployments de volta
```bash
kubectl scale deployment geoapi --replicas=3
kubectl scale deployment geoweb --replicas=2
```
- [ ] Aguardar pods ficarem Ready
- [ ] Executar smoke tests
```bash
curl -f https://api.carf.com.br/health
curl -f https://app.carf.com.br/
```
- [ ] Verificar métricas no Grafana (comparar com baseline)
- [ ] Desativar modo manutenção no load balancer
- [ ] Atualizar status page para operacional
- [ ] Notificar usuários que sistema está disponível

## Smoke Tests

```bash
# Health check dos serviços
curl -s https://api.carf.com.br/health | jq .status
curl -s https://keycloak.carf.com.br/health | jq .status

# Autenticação funciona
TOKEN=$(curl -s -X POST "https://keycloak.carf.com.br/realms/carf/protocol/openid-connect/token" \
  -d "grant_type=password&client_id=carf-web&username=test@test.com&password=test123" | jq -r .access_token)
[ -n "$TOKEN" ] && echo "Auth: OK" || echo "Auth: FAIL"

# API retorna dados
curl -s -H "Authorization: Bearer $TOKEN" https://api.carf.com.br/api/units?limit=1 | jq length
```

## Rollback

Se problemas críticos detectados:
```bash
# 1. Restaurar backup
pg_restore -h postgres -U carf -d carf -c pre_maintenance_20260116.dump

# 2. Reverter imagens de container
kubectl set image deployment/geoapi geoapi=carf/geoapi:previous-tag

# 3. Reiniciar pods
kubectl rollout restart deployment/geoapi
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
