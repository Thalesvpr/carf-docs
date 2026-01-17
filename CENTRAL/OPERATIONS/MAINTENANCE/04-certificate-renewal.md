# Certificate Renewal

Procedimentos para renovação de certificados TLS/SSL do CARF.

## Certificados Gerenciados

| Domínio | Tipo | Emissor | Auto-Renovação |
|---------|------|---------|----------------|
| api.carf.com.br | TLS | Let's Encrypt | Sim (cert-manager) |
| app.carf.com.br | TLS | Let's Encrypt | Sim (Vercel) |
| keycloak.carf.com.br | TLS | Let's Encrypt | Sim (cert-manager) |
| *.carf.com.br | Wildcard | DigiCert | Manual (anual) |

## Verificar Expiração

```bash
# Verificar certificado de endpoint
echo | openssl s_client -servername api.carf.com.br -connect api.carf.com.br:443 2>/dev/null | \
  openssl x509 -noout -dates

# Verificar todos certificados no cluster
kubectl get certificates -A -o custom-columns=NAME:.metadata.name,READY:.status.conditions[0].status,EXPIRY:.status.notAfter

# Alertar se expira em menos de 30 dias
kubectl get certificates -A -o json | jq -r '.items[] | select(.status.notAfter | fromdateiso8601 < (now + 2592000)) | .metadata.name'
```

## Renovação Automática (cert-manager)

cert-manager renova automaticamente 30 dias antes da expiração:

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: carf-api-tls
spec:
  secretName: carf-api-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - api.carf.com.br
  renewBefore: 720h  # 30 dias
```

## Renovação Manual (Wildcard)

Para certificado wildcard DigiCert (anual):

```bash
# 1. Gerar CSR
openssl req -new -newkey rsa:2048 -nodes \
  -keyout carf_wildcard.key \
  -out carf_wildcard.csr \
  -subj "/CN=*.carf.com.br/O=CARF/C=BR"

# 2. Submeter CSR no portal DigiCert

# 3. Após aprovação, baixar certificado e criar secret
kubectl create secret tls carf-wildcard-tls \
  --cert=carf_wildcard.crt \
  --key=carf_wildcard.key \
  -n carf

# 4. Reiniciar ingress controller
kubectl rollout restart deployment/ingress-nginx-controller -n ingress-nginx
```

## Troubleshooting

```bash
# Certificado não renovando automaticamente
kubectl describe certificate carf-api-tls -n carf
kubectl logs -l app=cert-manager -n cert-manager --tail=100

# Verificar challenge DNS/HTTP
kubectl get challenges -A
kubectl describe challenge <challenge-name>

# Forçar renovação
kubectl delete certificate carf-api-tls -n carf
# cert-manager recriará automaticamente
```

## Monitoramento

Alerta Prometheus quando certificado expira em menos de 14 dias:

```yaml
- alert: CertificateExpiringSoon
  expr: certmanager_certificate_expiration_timestamp_seconds - time() < 1209600
  for: 1h
  labels:
    severity: warning
  annotations:
    summary: "Certificado {{ $labels.name }} expira em menos de 14 dias"
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
