---
modules: [GEOAPI, GEOWEB]
epic: reliability
---

# RF-032: Redefinir Senha

Usuário que esqueceu senha pode solicitar redefinição via email onde fluxo inicia na tela de login com link "Esqueci minha senha" levando a formulário de recuperação solicitando email cadastrado, link de recuperação enviado automaticamente para email fornecido contendo URL única com token criptografado onde token possui expiração de 1 hora após geração invalidando automaticamente após esse período ou após uso bem-sucedido prevenindo reutilização maliciosa, validação de senha forte aplicada durante definição de nova senha exigindo mínimo 8 caracteres incluindo ao menos 1 letra maiúscula 1 minúscula 1 número e 1 caractere especial com feedback visual em tempo real indicando conformidade com cada critério conforme usuário digita, implementação em módulos GEOWEB para interface de usuário e GEOAPI para processamento backend incluindo geração de token seguro armazenamento temporário com TTL envio de email via serviço SMTP configurado validação de token em endpoint dedicado e sincronização de nova senha com Keycloak.

---

**Última atualização:** 2025-12-30
