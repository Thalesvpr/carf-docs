---
modules: [GEOAPI]
epic: performance
---

# RNF-019: Criptografia de Dados Sensíveis

O sistema GEOMAP5 deve garantir a proteção de dados sensíveis em repouso através de criptografia avançada utilizando o algoritmo AES-256, onde todos os dados pessoais identificáveis como CPF e CNPJ armazenados no banco de dados PostgreSQL devem ser criptografados antes de sua persistência, garantindo que mesmo em caso de acesso não autorizado ao banco de dados os dados permaneçam ilegíveis sem as chaves de criptografia apropriadas. As API keys utilizadas para autenticação de serviços devem ser armazenadas utilizando hashing forte com bcrypt, incluindo salt automático para cada chave, impedindo que as chaves originais sejam recuperadas mesmo que o banco de dados seja comprometido. Os backups automáticos do sistema, tanto incrementais diários quanto completos semanais, devem ser criptografados antes do armazenamento em repositórios externos, utilizando os mesmos padrões de criptografia AES-256, garantindo que os dados históricos mantêm o mesmo nível de proteção que os dados em produção. A implementação deve abranger tanto o módulo GEOAPI quanto a infraestrutura de banco de dados, permitindo que operações de leitura e escrita realizem automaticamente a criptografia e descriptografia conforme necessário, através de mecanismos transparentes que não impactem significativamente a performance do sistema. As chaves de criptografia devem ser gerenciadas de forma segura através de sistemas de gerenciamento de secrets como HashiCorp Vault ou AWS KMS, com rotação periódica configurável e auditoria de acesso às chaves, assegurando conformidade com requisitos de segurança e regulamentações como a LGPD. Este requisito é classificado como Must-have devido à criticidade da proteção de dados pessoais e à conformidade regulatória obrigatória para sistemas que manipulam informações sensíveis de cidadãos.
**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
