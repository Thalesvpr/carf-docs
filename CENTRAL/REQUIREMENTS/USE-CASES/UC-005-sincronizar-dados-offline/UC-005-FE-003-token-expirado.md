---
modules: [GEOWEB, REURBCAD]
epic: security
---

# UC-005-FE-003: Token Expirado

Fluxo de exceção do UC-005 Sincronizar Dados Offline ocorrendo no início da sincronização ou durante fase PULL/PUSH quando app envia request HTTP com header Authorization: Bearer {jwt_token} e servidor Keycloak valida token decodificando JWT verificando assinatura digital com public key e checando claim exp (expiration timestamp) comparando com tempo atual detectando exp < Date.now() indicando token expirado, servidor retorna HTTP 401 Unauthorized com response JSON contendo error="invalid_token" e error_description="Token has expired", onde app intercepta erro via axios.interceptors.response detectando status 401 e error code específico, verifica se refresh_token existe em SecureStore (AsyncStorage criptografado) armazenado durante login inicial, se refresh_token disponível app automaticamente dispara fluxo de renovação enviando POST /auth/realms/carf/protocol/openid-connect/token com body grant_type=refresh_token e refresh_token={stored_refresh_token}, Keycloak valida refresh_token verificando se não expirado (validade típica 30 dias vs access_token 15 minutos) e se válido retorna novo par access_token e refresh_token com expires_in indicando segundos até expiração, app atualiza SecureStore salvando novos tokens substituindo anteriores e retenta request original de sincronização usando novo access_token transparentemente sem interromper fluxo, se refresh_token também expirado ou inválido servidor retorna 401 novamente então app detecta falha definitiva de autenticação exibe modal vermelho "Sessão Expirada" com mensagem "Por favor faça login novamente para continuar" e botão Fazer Login redirecionando para tela de autenticação preservando dados pendentes localmente com needs_sync=true, após re-autenticação bem-sucedida app retorna automaticamente para tela de sincronização oferecendo retomar processo de onde parou garantindo segurança com tokens curtos minimizando janela de exposição enquanto mantém experiência fluida com refresh automático invisível ao usuário evitando interrupções desnecessárias em campo.

**Ponto de Desvio:** Início ou durante qualquer fase do UC-005 (validação de token em cada request)

**Retorno:** Se refresh sucesso continua transparente, se falha força re-login preservando pendências

---

**Última atualização:** 2025-12-30
