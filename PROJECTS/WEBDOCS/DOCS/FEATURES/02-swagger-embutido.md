---
status: review
updated: 2026-01-17
---

# Swagger Embutido

Seção /dev/swagger/ renderiza Swagger UI interativo permitindo desenvolvedores explorar e testar endpoints da GEOAPI diretamente no portal de documentação com autenticação real usando token JWT do usuário logado.

Componente SwaggerPage.astro verifica role dev antes de renderizar conteúdo. Usuários sem role recebem página 403 com explicação. Verificação acontece em middleware SSR antes de qualquer fetch de dados sensíveis como especificação OpenAPI.

Fetch da especificação executa durante SSR obtendo /swagger/v1/swagger.json da GEOAPI. Especificação é injetada como JSON inline no HTML evitando CORS issues e reduzindo latência de carregamento. Cache em memória de 5 minutos reduz carga no backend.

Inicialização do swagger-ui-dist acontece client-side após hidratação. Script configura spec com JSON inline, requestInterceptor adicionando Authorization header com token extraído de cookie, persistAuthorization false para não armazenar tokens no localStorage, e deepLinking true para URLs compartilháveis.

Customização visual via CSS sobrescreve cores do Swagger UI para manter consistência com tema CARF. Variáveis CSS mapeiam cores primárias, backgrounds, e tipografia. Header e topbar do Swagger são escondidos para não conflitar com navegação do WEBDOCS.

Try-it-out permite executar requisições reais contra GEOAPI usando token do desenvolvedor logado. Útil para testar endpoints durante desenvolvimento sem configurar ferramentas externas. Responses são exibidos com syntax highlighting e opção de copiar.
