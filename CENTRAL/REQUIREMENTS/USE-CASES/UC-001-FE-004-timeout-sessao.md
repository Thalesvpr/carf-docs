---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: security
---

# UC-001-FE-004: Timeout de Sessão

Fluxo de exceção do UC-001 Cadastrar Unidade Habitacional ocorrendo no passo 10 (salvamento no servidor) quando token JWT de autenticação expira durante operação após usuário permanecer inativo na tela de cadastro por tempo superior a TTL do access token (configurado em Keycloak tipicamente 5 minutos), onde ao tentar POST /api/units backend middleware de autenticação valida token decodificando JWT verificando assinatura e exp claim, detecta expiração retornando HTTP 401 Unauthorized com body `{"error": "Token expired", "code": "TOKEN_EXPIRED"}`, e frontend interceptor HTTP (Axios ou Fetch) captura erro 401 antes de propagar para componente verificando se código específico é TOKEN_EXPIRED diferenciando de credenciais inválidas. Sistema tenta renovação automática de token enviando refresh token armazenado em httpOnly cookie ou sessionStorage seguro para endpoint POST /api/auth/refresh que valida refresh token contra Keycloak, se refresh token ainda válido (TTL tipicamente 30 minutos) Keycloak retorna novo access token e sistema atualiza automaticamente header Authorization das próximas requisições re-tentando operação original POST /api/units de forma transparente sem intervenção do usuário que percebe apenas leve delay adicional, e se renovação bem-sucedida unidade é salva normalmente prosseguindo para passo 11 do fluxo principal. Porém se refresh token também expirou (usuário inativo >30 minutos) ou foi revogado (logout em outro dispositivo SSO logout global) renovação falha retornando 401 e sistema precisa forçar re-autenticação completa, antes de redirecionar para login sistema salva dados preenchidos no formulário em localStorage ou sessionStorage usando chave temporária `pending_unit_${timestamp}` contendo JSON completo com código endereço geometria tipo observações permitindo recuperação após login, exibe modal "Sessão expirada. Você será redirecionado para login. Seus dados foram salvos e serão recuperados após autenticação" com countdown de 5 segundos ou botão Fazer Login Agora, redireciona para tela de login preservando return_url atual na query string, após usuário autenticar novamente com Keycloak sistema redireciona de volta para tela de cadastro verificando localStorage por chave `pending_unit_*`, se encontra dados salvos exibe toast "Recuperando dados salvos..." e pré-preenche formulário automaticamente restaurando todos campos incluindo geometria renderizada no mapa, e usuário revisa dados verificando se tudo está correto (possível que dados no servidor mudaram durante tempo offline) e clica Salvar novamente concluindo operação.

**Ponto de Desvio:** Passo 10 do UC-001 (salvamento no servidor quando token expirado)

**Detecção de Expiração:**
```typescript
// Axios interceptor
axios.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401 && error.response?.data?.code === 'TOKEN_EXPIRED') {
      // Tentar renovação automática
      try {
        const newToken = await refreshAccessToken();
        // Re-tentar requisição original com novo token
        error.config.headers.Authorization = `Bearer ${newToken}`;
        return axios.request(error.config);
      } catch (refreshError) {
        // Refresh falhou, forçar re-login
        saveFormDataToLocalStorage();
        redirectToLogin();
      }
    }
    return Promise.reject(error);
  }
);
```

**Renovação Automática (Sucesso):**
1. Interceptor detecta 401 TOKEN_EXPIRED
2. POST /api/auth/refresh com refresh token
3. Keycloak retorna novo access token (200 OK)
4. Atualiza header Authorization
5. Re-tenta POST /api/units original
6. Unidade salva normalmente (transparente para usuário)

**Renovação Falhou (Refresh Expirado):**
1. POST /api/auth/refresh retorna 401
2. Sistema salva dados formulário em localStorage:
```typescript
localStorage.setItem(`pending_unit_${Date.now()}`, JSON.stringify({
  code: formData.code,
  address: formData.address,
  geometry: formData.geometry,
  type: formData.type,
  observations: formData.observations,
  savedAt: new Date().toISOString()
}));
```
3. Exibe modal "Sessão expirada" com countdown 5s
4. Redireciona para /login?return_url=/units/new
5. Após login, verifica localStorage por `pending_unit_*`
6. Restaura dados no formulário automaticamente
7. Usuário revisa e salva novamente

**Retorno:**
- Se renovação automática sucesso: Prossegue para passo 11 do UC-001 (sucesso)
- Se renovação falhou: Re-autentica, restaura dados, volta ao passo 8 (usuário salva novamente)

---

**Última atualização:** 2025-12-30
