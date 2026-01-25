---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-018: HTTPS Obrigatorio

## Descricao

Toda comunicacao entre clientes e servidores deve utilizar HTTPS com TLS 1.2 ou superior. Protege dados em transito contra interceptacao e ataques man-in-the-middle.

## Metricas

- Protocolo: TLS 1.2+ obrigatorio
- Certificado: SSL valido de CA confiavel
- Header HSTS: habilitado

## Criterios de Aceitacao

1. Certificado SSL valido em producao (nao autoassinado)
2. Redirect automatico HTTP para HTTPS (301/308)
3. HSTS habilitado com max-age adequado
