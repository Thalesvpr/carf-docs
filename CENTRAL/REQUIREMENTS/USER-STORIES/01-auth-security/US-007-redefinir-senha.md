---
modules: [GEOAPI, GEOWEB]
epic: security
---

# US-007: Redefinir Senha

Como usuário que esqueceu senha, quero receber email para redefinir senha para que eu recupere acesso à minha conta, onde o fluxo de recuperação implementa o padrão seguro de reset via token temporário enviado por email, garantindo que apenas o proprietário legítimo da conta possa redefinir a senha. O cenário principal de uso inicia quando o usuário clica no link "Esqueci minha senha" na tela de login e fornece seu endereço de email cadastrado, permitindo que o sistema gere um token único e criptograficamente seguro que é enviado via email para o endereço fornecido, onde o email contém um link com o token que direciona para uma página de redefinição de senha que valida o token antes de permitir que o usuário defina uma nova senha. Os critérios de aceitação incluem o fluxo completo de "Esqueci minha senha" funcional com validação de email existente no sistema, o envio de email contendo um token único e impossível de adivinhar gerado com algoritmo criptográfico seguro, a expiração automática do token após 1 hora para limitar janela de vulnerabilidade, e a atualização bem-sucedida da senha no Keycloak quando o usuário submete nova senha válida através do link com token válido. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoints POST /api/auth/forgot-password para solicitar reset e POST /api/auth/reset-password para executar a mudança, integrando com Keycloak e serviço de email) e GEOWEB (páginas de solicitação de reset e formulário de nova senha), garantindo rastreabilidade com RF-032 (Recuperação de Senha) e UC-001 (Caso de Uso de Autenticação), onde a segurança é mantida através de tokens de uso único que se invalidam após uso ou expiração, incluindo proteção contra ataques de enumeração de usuários e rate limiting para prevenir abuso.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Review
