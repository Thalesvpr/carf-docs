---
modules: [GEOAPI, GEOWEB]
epic: communities
---

# RF-158: Editar Levantamento

Este requisito especifica que usuários autorizados devem poder editar dados de levantamentos topográficos existentes permitindo correção de metadados e atualização de arquivos conforme necessário, onde interface oferece acesso a todos os campos configuráveis do registro. O sistema deve permitir atualização de campos descritivos incluindo data do levantamento responsável técnico equipamento utilizado e vinculação a comunidade ou unidade, onde usuário acessa formulário de edição populado com valores atuais modifica campos desejados e salva alterações que são validadas e persistidas no backend. O sistema deve suportar re-upload de arquivos brutos permitindo substituir arquivo original por versão corrigida ou complementar, onde novo upload pode sobrescrever arquivo anterior ou ser adicionado como versão adicional conforme implementação de versionamento, garantindo que dados mais recentes ou corretos estejam disponíveis sem perda de histórico se aplicável. Todas as alterações realizadas devem gerar entradas detalhadas no log de alterações vinculado ao levantamento registrando usuário responsável pela edição timestamp preciso descrição de campos modificados e valores anteriores versus novos, garantindo rastreabilidade completa de evolução dos dados do levantamento e permitindo auditoria de modificações. O sistema deve validar dados editados garantindo consistência e integridade antes de aceitar mudanças. A funcionalidade deve estar disponível nos módulos GEOWEB através de interface de edição e GEOAPI via endpoint PATCH com validações apropriadas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
