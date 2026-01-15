---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: security
---

# RF-016: Auditoria de Acessos

Sistema deve registrar logs detalhados de login logout e tentativas falhadas de autenticação onde cada evento captura timestamp preciso com timezone identificador único de usuário (user_id ou email) endereço IP de origem user-agent do navegador ou aplicativo e resultado da tentativa (sucesso falha), logs de tentativas de acesso negado incluem informação adicional sobre motivo da negação (senha incorreta usuário bloqueado token inválido permissão insuficiente) recurso que tentou acessar e contexto relevante para análise de segurança e troubleshooting, retenção de logs por período mínimo de 12 meses conforme requisitos de compliance e regulamentação de proteção de dados onde logs armazenados de forma segura com integridade garantida preferencialmente em storage append-only ou sistema de logging centralizado com proteção contra adulteração, implementação em módulo GEOAPI integrando com solução de logging estruturado (Elasticsearch Splunk CloudWatch Logs) permitindo queries complexas agregações e criação de alertas automatizados para detecção de comportamentos suspeitos como múltiplas tentativas falhadas de login acessos em horários atípicos ou padrões anômalos de utilização.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
