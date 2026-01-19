# Integração com GEOAPI Swagger

Seção /dev/swagger/ do WEBDOCS renderiza documentação interativa da API GEOAPI consumindo especificação OpenAPI diretamente do backend. Integração permite testar endpoints usando token JWT real do desenvolvedor logado.

Especificação OpenAPI é gerada automaticamente pela GEOAPI via Swashbuckle a partir dos controllers .NET com XML comments. Endpoint /swagger/v1/swagger.json retorna JSON atualizado refletindo estado atual da API sem necessidade de manutenção manual de documentação.

Componente SwaggerEmbed.astro executa fetch da especificação durante SSR, inicializa swagger-ui-dist com spec inline, e configura requestInterceptor para adicionar header Authorization: Bearer com token do usuário extraído do cookie de sessão. Try-it-out funciona com autenticação real.

Customização visual aplica tema CARF ao Swagger UI via CSS sobrescrevendo cores padrão para manter consistência com restante do portal. Header e footer do Swagger são escondidos via CSS para não conflitar com layout do WEBDOCS.

Autorização verifica role dev antes de renderizar componente. Usuários sem role recebem mensagem explicando necessidade de acesso de desenvolvedor. Isso previne exposição acidental de endpoints internos ou sensíveis para usuários não autorizados.

Cache da especificação armazenada em memória por 5 minutos reduz carga no backend para usuários que navegam entre páginas. Invalidação manual via query param ?refresh=true força novo fetch para desenvolvedores testando mudanças recentes.

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
