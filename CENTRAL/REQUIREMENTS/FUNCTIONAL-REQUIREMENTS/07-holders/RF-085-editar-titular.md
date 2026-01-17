---
modules: [GEOWEB, REURBCAD]
epic: holders
---

# RF-085: Editar Titular

O sistema deve permitir que usuários editem dados cadastrais de titulares existentes, onde interface oferece formulário preenchido com valores atuais possibilitando atualização de qualquer campo incluindo nome, documentos, contatos e endereço. Todas as alterações realizadas são automaticamente registradas em log de auditoria capturando timestamp, usuário responsável pela modificação, campos alterados e valores anteriores e novos, garantindo rastreabilidade completa do histórico de mudanças e possibilitando eventual reversão ou análise forense de modificações inadequadas. As mesmas validações aplicadas durante criação são reaplicadas na edição incluindo verificação algorítmica de CPF/CNPJ quando documentos são modificados, validação de formato de email e telefone, e verificação de duplicidade se número de documento for alterado prevenindo que edição crie conflito com titular previamente existente. Implementado nos módulos GEOWEB e GEOAPI com prioridade Must-have, este recurso é essencial para manutenção evolutiva do cadastro permitindo correção de erros de digitação, atualização de informações de contato quando titulares mudam telefone ou email, e complementação gradual de dados quando informações adicionais tornam-se disponíveis após cadastramento inicial realizado com dados parciais coletados em campo.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
