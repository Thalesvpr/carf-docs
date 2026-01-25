---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-016: Auditoria de Acessos

## Descricao

Sistema deve registrar logs detalhados de login, logout e tentativas falhadas de autenticacao. Cada evento captura timestamp, identificador de usuario, IP de origem, user-agent e resultado. Logs de acesso negado incluem motivo da negacao e recurso tentado. Retencao minima de 12 meses conforme requisitos de compliance.

## Criterios de Aceitacao

1. Login, logout e falhas registrados em log de auditoria
2. Captura de timestamp, user_id, IP, user-agent
3. Motivo de negacao registrado para acessos bloqueados
4. Retencao de logs por minimo 12 meses
5. Integracao com sistema de logging centralizado

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-005, RF-012
