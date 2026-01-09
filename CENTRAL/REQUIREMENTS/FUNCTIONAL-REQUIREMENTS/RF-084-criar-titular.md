---
modules: [GEOWEB]
epic: holders
---

# RF-084: Criar Titular

O sistema deve permitir que usuários cadastrem novos titulares representando pessoas físicas ou jurídicas responsáveis por unidades habitacionais, onde formulário captura campos essenciais como nome completo ou razão social, CPF ou CNPJ conforme tipo de pessoa, e informações de contato incluindo telefone e email. A validação de CPF e CNPJ utiliza algoritmo de verificação de dígitos garantindo que apenas documentos válidos matematicamente sejam aceitos, apresentando mensagem de erro clara quando número informado não passa em verificação algorítmica de consistência. Sistema implementa verificação de duplicidade consultando base existente de titulares antes de permitir criação, alertando usuário quando CPF ou CNPJ informado já existe no cadastro e oferecendo opção de vincular titular existente ao invés de criar duplicata desnecessária. Implementado nos módulos GEOWEB, REURBCAD e GEOAPI com prioridade Must-have, este recurso é fundamental para gestão de responsabilidades sobre unidades onde titulares podem ser proprietários formais, possuidores de fato, usufrutuários ou outras categorias de relacionamento jurídico e social com imóveis cadastrados, garantindo identificação clara de pessoas vinculadas a cada unidade e possibilitando comunicação, notificação e reconhecimento de direitos ao longo do processo de regularização fundiária.

---

**Última atualização:** 2025-12-30
