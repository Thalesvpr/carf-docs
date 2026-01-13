---
modules: [GEOAPI, REURBCAD]
epic: compatibility
---

# RF-125: Limite de Armazenamento por Tenant

Este requisito estabelece que cada tenant deve ter quota configurável de armazenamento em disco para controlar uso de recursos e implementar modelo de precificação ou governança baseado em consumo, onde administrador do sistema pode definir limite máximo de bytes que tenant pode utilizar. O modelo de dados de tenants deve incluir campo storage_quota armazenando limite em bytes ou unidade equivalente, onde valor pode ser configurado individualmente para cada tenant conforme plano contratado ou política interna, permitindo flexibilidade na alocação de recursos. O sistema deve implementar cálculo contínuo ou periódico de uso atual de storage por tenant somando tamanho de todos os arquivos documentos e fotos associados direta ou indiretamente ao tenant através de suas entidades, onde cálculo pode ser executado em tempo real durante uploads ou através de job batch que atualiza periodicamente métricas de uso. Quando tenant atinge ou excede limite configurado, o sistema deve bloquear novos uploads retornando erro claro informando que quota foi excedida, onde mensagem orienta usuário a contatar administrador ou liberar espaço excluindo arquivos desnecessários antes de tentar novo upload. O sistema deve expor métrica de uso atual versus quota através de endpoint da API e painel administrativo. A funcionalidade deve ser implementada no módulo GEOAPI através de validações antes de aceitar uploads.

---

**Última atualização:** 2025-12-30