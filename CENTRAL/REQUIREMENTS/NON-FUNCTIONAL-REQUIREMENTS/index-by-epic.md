# Requisitos Não-Funcionais por Épica
Índice dos 85 requisitos não-funcionais do sistema CARF organizados por épica arquitetural com métricas e critérios de aceitação.
---

## Security (24 RNFs)
- [RNF-007: Exportação de Dados](./RNF-007-exportacao-dados.md) - GEOGIS
- [RNF-016: Autenticação OAuth2](./RNF-016-autenticacao-oauth2.md) - GEOWEB
- [RNF-017: Expiração de Tokens](./RNF-017-expiracao-tokens.md) - GEOAPI, GEOWEB, REURBCAD
- [RNF-018: HTTPS Obrigatório](./RNF-018-https-obrigatorio.md) - GEOWEB
- [RNF-020: Validação de Input](./RNF-020-validacao-input.md) - GEOAPI, GEOWEB
- [RNF-022: CORS Restritivo](./RNF-022-cors-restritivo.md) - GEOAPI, REURBCAD
- [RNF-023: Content Security Policy](./RNF-023-content-security-policy.md) - GEOAPI
- [RNF-025: Isolamento de Tenants](./RNF-025-isolamento-tenants.md) - GEOAPI
- [RNF-027: Armazenamento Seguro de Senhas](./RNF-027-armazenamento-seguro-senhas.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-028: Proteção de API Keys](./RNF-028-protecao-api-keys.md) - GEOAPI, GEOWEB
- [RNF-029: Scan de Malware em Uploads](./RNF-029-scan-malware-uploads.md) - GEOAPI
- [RNF-030: Proteção de Dados Pessoais (LGPD)](./RNF-030-protecao-dados-pessoais-lgpd.md) - GEOAPI, GEOWEB
- [RNF-031: Timeout de Sessão](./RNF-031-timeout-sessao.md) - GEOWEB, REURBCAD
- [RNF-033: Secrets Management](./RNF-033-secrets-management.md) - GEOAPI
- [RNF-034: SQL Injection Prevention](./RNF-034-sql-injection-prevention.md) - GEOAPI
- [RNF-035: Monitoramento de Segurança](./RNF-035-monitoramento-seguranca.md) - GEOAPI
- [RNF-043: Monitoramento de Erros](./RNF-043-monitoramento-erros-aplicacao.md) - GEOAPI, GEOWEB, REURBCAD
- [RNF-050: Mensagens de Erro Claras](./RNF-050-mensagens-erro-claras.md) - GEOWEB, REURBCAD
- [RNF-060: Ambiente de Desenvolvimento Replicável](./RNF-060-ambiente-de-desenvolvimento-replicavel.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-063: Tratamento de Exceções](./RNF-063-tratamento-de-excecoes.md) - GEOAPI, GEOWEB
- [RNF-064: Refatoração Contínua](./RNF-064-refatoracao-continua.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-085: API REST Padrão](./RNF-085-api-rest-padrao.md) - GEOAPI
- [RNF-086: OpenAPI Spec](./RNF-086-openapi-spec.md) - GEOAPI, GEOWEB
- [RNF-088: OAuth2 Providers](./RNF-088-oauth2-providers.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS

## Scalability (20 RNFs)
- [RNF-006: Upload de Arquivos](./RNF-006-upload-arquivos.md) - GEOWEB, REURBCAD
- [RNF-009: Sincronização Offline - Push](./RNF-009-sincronizacao-offline-push.md) - GEOAPI, REURBCAD
- [RNF-012: Cache de Dados](./RNF-012-cache-dados.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-013: Consumo de Memória - Backend](./RNF-013-consumo-memoria-backend.md) - GEOAPI
- [RNF-021: Rate Limiting](./RNF-021-rate-limiting.md) - GEOAPI
- [RNF-026: Proteção contra CSRF](./RNF-026-protecao-csrf.md) - GEOAPI, GEOWEB, REURBCAD
- [RNF-032: Permissões Granulares](./RNF-032-permissoes-granulares.md) - GEOAPI, GEOWEB
- [RNF-036: Uptime](./RNF-036-uptime.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-061: Observabilidade](./RNF-061-observabilidade.md) - GEOAPI
- [RNF-071: Escala Horizontal - Backend](./RNF-071-escala-horizontal-backend.md) - GEOAPI
- [RNF-072: Usuários Simultâneos](./RNF-072-usuarios-simultaneos.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-073: Volume de Dados - Unidades](./RNF-073-volume-de-dados-unidades.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-074: Volume de Dados - Arquivos](./RNF-074-volume-dados-arquivos.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-075: Pico de Carga](./RNF-075-pico-carga.md) - REURBCAD
- [RNF-076: Conexões de Banco](./RNF-076-conexoes-banco.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-077: Cache Distribuído](./RNF-077-cache-distribuido.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-078: Job Queue](./RNF-078-job-queue.md) - GEOWEB
- [RNF-079: Rate de Sincronização](./RNF-079-rate-sincronizacao.md) - GEOAPI, REURBCAD
- [RNF-080: Database Sharding (Futuro)](./RNF-080-database-sharding.md) - GEOAPI
- [RNF-087: Webhooks (Futuro)](./RNF-087-webhooks.md) - GEOAPI, GEOWEB

## Performance (19 RNFs)
- [RNF-001: Tempo de Resposta - Endpoints de Leitura](./RNF-001-tempo-resposta-endpoints-leitura.md) - GEOAPI
- [RNF-002: Tempo de Resposta - Endpoints de Escrita](./RNF-002-tempo-resposta-endpoints-escrita.md) - GEOAPI
- [RNF-003: Tempo de Resposta - Queries Espaciais](./RNF-003-tempo-resposta-queries-espaciais.md) - GEOAPI
- [RNF-004: Tempo de Carregamento - Frontend](./RNF-004-tempo-carregamento-frontend.md) - GEOWEB
- [RNF-005: Tempo de Carregamento - Mapa](./RNF-005-tempo-carregamento-mapa.md) - GEOWEB
- [RNF-010: Renderização de Geometrias](./RNF-010-renderizacao-geometrias.md) - GEOWEB
- [RNF-011: Paginação de Listagens](./RNF-011-paginacao-listagens.md) - GEOAPI
- [RNF-015: Tamanho do Bundle - Frontend](./RNF-015-tamanho-bundle-frontend.md) - GEOWEB
- [RNF-019: Criptografia de Dados Sensíveis](./RNF-019-criptografia-dados-sensiveis.md) - GEOAPI
- [RNF-024: Auditoria de Ações](./RNF-024-auditoria-acoes.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-038: Backup de Dados](./RNF-038-backup-automatico-dados.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-039: RPO (Recovery Point Objective)](./RNF-039-rpo-objetivo-ponto-recuperacao.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-041: Graceful Degradation](./RNF-041-degradacao-graciosa-sistema.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-042: Zero Downtime Deployment](./RNF-042-deploy-zero-downtime.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-045: Validação de Integridade](./RNF-045-validacao-integridade-dados.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-049: Feedback Visual](./RNF-049-feedback-visual-operacoes.md) - GEOAPI, GEOWEB
- [RNF-054: Busca Intuitiva](./RNF-054-busca-intuitiva-autocomplete.md) - GEOAPI, GEOWEB, REURBCAD
- [RNF-059: Versionamento Semântico](./RNF-059-versionamento-semantico.md) - GEOAPI, GEOWEB
- [RNF-084: Integração WMS/WMTS](./RNF-084-integracao-wms-wmts.md) - GEOWEB, GEOGIS

## Usability (10 RNFs)
- [RNF-014: Consumo de Memória - Mobile](./RNF-014-consumo-memoria-mobile.md) - GEOWEB, REURBCAD
- [RNF-046: Responsividade - Web](./RNF-046-responsividade-web.md) - GEOWEB, REURBCAD, GEOGIS
- [RNF-047: Internacionalização](./RNF-047-internacionalizacao-i18n.md) - GEOAPI, GEOWEB, REURBCAD
- [RNF-048: Acessibilidade (WCAG 2.1)](./RNF-048-acessibilidade-wcag.md) - GEOWEB, REURBCAD
- [RNF-052: Consistência de UI](./RNF-052-consistencia-ui-design-system.md) - GEOAPI, GEOWEB
- [RNF-053: Onboarding](./RNF-053-onboarding-tour-guiado.md) - GEOAPI, GEOWEB, REURBCAD
- [RNF-057: Documentação de Código](./RNF-057-documentacao-de-codigo.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-062: Modularidade](./RNF-062-modularidade.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-089: Timezone](./RNF-089-timezone.md) - GEOAPI, GEOWEB
- [RNF-090: Charset](./RNF-090-charset.md) - GEOAPI

## Compatibility (5 RNFs)
- [RNF-008: Sincronização Offline - Pull](./RNF-008-sincronizacao-offline-pull.md) - GEOAPI, REURBCAD
- [RNF-044: Logs Estruturados](./RNF-044-logs-estruturados-centralizados.md) - REURBCAD
- [RNF-058: Linting e Formatação](./RNF-058-linting-e-formatacao.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-081: Formatos de Importação](./RNF-081-formatos-importacao.md) - GEOWEB, GEOGIS
- [RNF-083: Sistemas de Coordenadas](./RNF-083-sistemas-coordenadas.md) - GEOWEB, REURBCAD

## Reliability (5 RNFs)
- [RNF-037: Recuperação de Falhas](./RNF-037-recuperacao-automatica-falhas.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-040: RTO (Recovery Time Objective)](./RNF-040-rto-objetivo-tempo-recuperacao.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-051: Undo/Redo](./RNF-051-undo-redo-acoes.md) - GEOAPI, GEOWEB
- [RNF-055: Atalhos de Teclado](./RNF-055-atalhos-teclado.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS
- [RNF-065: Rollback de Deploy](./RNF-065-rollback-de-deploy.md) - GEOAPI, GEOWEB, REURBCAD, GEOGIS

## Maintainability (2 RNFs)
- [RNF-056: Cobertura de Testes](./RNF-056-cobertura-de-testes.md) - GEOAPI, GEOWEB
- [RNF-082: Formatos de Exportação](./RNF-082-formatos-exportacao.md) - GEOWEB, GEOGIS

---
**Última atualização:** 2026-01-10
