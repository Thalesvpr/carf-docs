---
id: RNF-031
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-031: Timeout de Sessao

## Descricao

GEOWEB e REURBCAD devem implementar timeout automatico de sessoes inativas. Previne acesso nao autorizado quando usuarios deixam dispositivos desacompanhados.

## Metricas

- Timeout: 30 minutos de inatividade
- Aviso: 2 minutos antes da expiracao
- Configuracao: externalizavel por ambiente

## Criterios de Aceitacao

1. Logout automatico apos 30 minutos sem interacao
2. Modal de aviso aos 28 minutos com opcao "Continuar conectado"
3. Redirect para login com mensagem clara apos timeout
