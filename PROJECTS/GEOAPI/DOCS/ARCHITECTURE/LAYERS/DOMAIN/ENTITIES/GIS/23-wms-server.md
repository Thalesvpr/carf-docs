# WmsServer

Entidade representando servidor WMS Web Map Service externo configurado sistema permitindo exibir camadas base órgãos oficiais IBGE INPE ou prefeituras fornecendo contexto cartográfico sem armazenar dados localmente. Herda de BaseEntity fornecendo auditoria soft delete. Campos principais incluem TenantId Guid FK Tenant isolando configurações cliente, Name string identificador (IBGE WMS, Prefeitura XYZ), BaseUrl string URL serviço WMS, Version string protocolo (1.1.1 ou 1.3.0) e Username Password string nullable autenticação básica credenciais criptografadas.

Campos controle incluem IsActive bool servidor ativo uso, LastSync DateTime nullable última vez GetCapabilities executado, Capabilities XML nullable resposta armazenado consulta offline metadados e ConnectionTimeout int segundos padrão 30. Métodos incluem TestConnection() validando servidor responde, SyncCapabilities() fazendo GetCapabilities parseando XML criando/atualizando WmsLayer correspondentes, Activate()/Deactivate() controlando IsActive e UpdateCredentials(username password) criptografando senha.

Relacionamento principal WmsLayer através coleção Layers cada servidor múltiplas camadas descobertas GetCapabilities. Integra frontend GEOWEB adicionando tile layer Mapbox/Leaflet requests GetMap renderizar imagens, suporta autenticação básica HTTP e dispara sincronização periódica background job Hangfire SyncCapabilities semanalmente mantendo lista camadas atualizada.

---

**Última atualização:** 2026-01-12
