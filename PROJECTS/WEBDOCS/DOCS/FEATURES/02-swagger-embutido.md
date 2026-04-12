---
type: leaf
status: review
updated: 2026-02-07
---

# Swagger Embutido

Secao /dev/swagger/ renderiza Swagger UI interativo permitindo desenvolvedores explorar e testar endpoints da GEOAPI diretamente no portal de documentacao com autenticacao real usando token JWT do usuario logado.

Componente SwaggerPage.astro verifica role dev antes de renderizar conteudo. Usuarios sem role recebem pagina 403 com explicacao. Verificacao acontece em middleware SSR antes de qualquer fetch de dados sensiveis como especificacao OpenAPI.

Fetch da especificacao executa durante SSR obtendo /swagger/v1/swagger.json da GEOAPI. Especificacao e injetada como JSON inline no HTML evitando CORS issues e reduzindo latencia de carregamento. Cache em memoria de 5 minutos reduz carga no backend.

Inicializacao do swagger-ui-dist acontece client-side apos hidratacao. Script configura spec com JSON inline, requestInterceptor adicionando Authorization header com token extraido de cookie, persistAuthorization false para nao armazenar tokens no localStorage, e deepLinking true para URLs compartilhaveis.

Customizacao visual via CSS sobrescreve cores do Swagger UI para consistencia com tema CARF. Topbar escondido. Cores por metodo HTTP: azul GET, verde POST, laranja PUT, vermelho DELETE. Tema escuro ajusta para variantes Starlight.

Try-it-out permite requisicoes reais contra GEOAPI usando token do desenvolvedor logado.

Detalhes de componente, cache e layout em 02-swagger-embutido-detalhes.md.
