---
modules: [GEOWEB]
epic: security
---

# RF-015: Sessão Expirada - Redirecionamento

Sistema deve detectar quando sessão expirou e tentativa de renovação via refresh_token falhou indicando necessidade de re-autenticação completa onde detecção ocorre através de captura de resposta HTTP 401 Unauthorized combinada com falha subsequente ao tentar renovar usando refresh_token, mensagem clara ao usuário deve ser exibida explicando que sessão expirou por inatividade prolongada ou timeout de segurança e solicitando novo login utilizando linguagem amigável como "Sua sessão expirou por segurança. Por favor, faça login novamente." evitando jargões técnicos assustadores, funcionalidade de retorno à tela original após re-login implementada salvando URL ou rota atual antes de redirecionar para login onde após autenticação bem-sucedida sistema restaura contexto anterior permitindo usuário continuar trabalho de onde parou sem perda de contexto, implementação em módulos GEOWEB e REURBCAD utilizando guards de rota ou interceptors HTTP que gerenciam fluxo de redirecionamento preservando deep links e query parameters quando apropriado.

---

**Última atualização:** 2025-12-30
