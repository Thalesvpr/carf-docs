---
modules: [GEOAPI, GEOWEB]
epic: security
---

# US-005: Criar API Key

Como administrador, quero gerar API keys para integrações para que sistemas externos acessem a API, onde o processo de criação gera chaves criptográficas seguras que permitem autenticação de aplicações e serviços externos sem expor credenciais de usuários humanos, garantindo rastreabilidade e controle sobre acessos programáticos ao sistema. O cenário principal de uso inicia quando um administrador acessa o painel de gerenciamento de API keys e solicita a criação de uma nova chave fornecendo um nome descritivo e selecionando permissões específicas que limitam o escopo de acesso, permitindo que o sistema gere um par de identificadores incluindo um API Key ID (público) e um Secret (privado) onde o secret é exibido apenas uma única vez durante a criação e nunca mais é recuperável. Os critérios de aceitação incluem a geração de API key com nome descritivo e conjunto configurável de permissões granulares, a exibição do secret apenas uma vez imediatamente após criação com aviso claro de que não será mostrado novamente, o armazenamento seguro onde o secret é mantido com hash criptográfico (bcrypt ou similar) e nunca em plain-text no banco de dados, e a configuração de expiração opcional onde o administrador pode definir data de validade ou deixar a key permanente. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint POST /api/auth/api-keys com lógica de geração e armazenamento seguro) e GEOWEB (interface de gerenciamento de API keys), garantindo rastreabilidade com RF-003 (Gestão de API Keys), onde cada key criada é associada ao tenant e permite auditoria completa de todas as operações realizadas através dela, incluindo rate limiting e possibilidade de revogação imediata se comprometida.

---

**Última atualização:** 2025-12-30