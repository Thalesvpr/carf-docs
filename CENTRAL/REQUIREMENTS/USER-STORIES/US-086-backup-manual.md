---
modules: [GEOAPI, GEOWEB]
epic: security
---

# US-086: Backup Manual

Como super administrador do sistema, quero gerar backup manual completo dos dados do tenant para que segurança informacional seja garantida, permitindo recuperação de desastres, migração de ambientes ou arquivamento de marcos regulatórios. A funcionalidade deve disponibilizar botão claramente identificado Criar Backup na interface administrativa permitindo acionamento sob demanda de processo de backup completo incluindo banco de dados relacional, arquivos de geometrias geoespaciais, documentos anexados (PDFs, imagens) e configurações do tenant. O sistema deve executar processamento assíncrono do backup devido ao volume potencialmente grande de dados, evitando bloqueio da interface durante operação que pode levar vários minutos dependendo da quantidade de informações armazenadas. Deve ser implementado mecanismo de notificação automática informando conclusão do backup através de email, notificação push na interface ou ambos, incluindo informações de tamanho do arquivo gerado, tempo de processamento e hash de integridade. Após conclusão, arquivo de backup deve ficar disponível para download seguro durante período configurável, com autenticação obrigatória e registro em audit log de todas as operações de geração e download de backups. Os critérios de aceitação incluem botão Criar Backup acessível apenas a super administradores, execução em background com job assíncrono rastreável, notificação multi-canal ao completar incluindo link de download, e disponibilização de arquivo criptografado com prazo de validade configurável. Esta User Story é implementada através do endpoint POST /api/tenants/{id}/backups no backend GEOAPI utilizando jobs distribuídos, e painel administrativo no frontend GEOWEB, pertencendo ao Epic 11: Administração. O status atual é implemented, com testes validando integridade dos backups gerados e processo de recuperação.

---

**Última atualização:** 2025-12-30
