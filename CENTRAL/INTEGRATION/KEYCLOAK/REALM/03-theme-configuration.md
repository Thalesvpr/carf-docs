---
status: review
updated: 2026-01-19
---

# Configuração de Tema no Realm

Configuração de temas no realm CARF controla aparência visual das páginas de autenticação exibidas aos usuários durante login logout registro reset-password, definindo propriedade loginTheme no realm settings que referencia nome do tema instalado em /opt/keycloak/themes/, realm CARF configurado com loginTheme="carf" aplicando tema customizado split-screen verde institucional para todas páginas de autenticação incluindo login.ftl register.ftl login-reset-password.ftl error.ftl info.ftl.

Configuração via Admin Console acessando Realm Settings do realm "carf", aba Themes apresenta dropdowns Login Theme Account Theme Email Theme Admin Console Theme, selecionar "carf" para Login Theme aplica tema customizado CARF nas páginas de autenticação, Account Theme define aparência do console de conta do usuário /realms/carf/account, Email Theme define templates de emails transacionais, salvar alterações clicando Save, alterações aplicadas imediatamente para novos acessos sem necessidade de restart.

Configuração via Admin API alternativa programática usando endpoint PUT /admin/realms/carf enviando JSON body com campo "loginTheme": "carf", útil para automação Terraform scripts deployment pipelines CI/CD, exemplo curl -X PUT "http://localhost:8080/admin/realms/carf" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"loginTheme": "carf"}', recuperar configuração atual GET /admin/realms/carf retorna objeto realm incluindo loginTheme accountTheme emailTheme.

Cache de temas em desenvolvimento deve ser desabilitado para permitir hot-reload de alterações CSS JavaScript via variáveis ambiente KC_SPI_THEME_CACHE_THEMES=false KC_SPI_THEME_STATIC_MAX_AGE=-1 no docker-compose.dev.yml, templates FreeMarker .ftl ainda requerem restart container mesmo com cache desabilitado, acessar /admin/realms/carf/events/config na Admin Console e clicar "Clear caches" também força reload temas.

Cache de temas em produção deve ser habilitado para performance via KC_SPI_THEME_CACHE_THEMES=true KC_SPI_THEME_STATIC_MAX_AGE=2592000 (30 dias em segundos), temas são compilados e cacheados na primeira requisição, alterações requerem restart do Keycloak ou clear manual do cache, imagem Docker de produção inclui tema CARF pré-instalado eliminando necessidade de volume mounts.

Instalação tema customizado requer arquivos do tema presentes em /opt/keycloak/themes/carf/ no container Keycloak, desenvolvimento usa volume mount mapeando diretório local, produção usa COPY no Dockerfile da imagem customizada, após instalação tema aparece automaticamente nos dropdowns do Admin Console, implementação completa do tema CARF em [PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/themes/carf/](../../../../PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/themes/carf/).

Referências [06-login-theme-carf](../../../../PROJECTS/KEYCLOAK/DOCS/FEATURES/06-login-theme-carf.md) documentação detalhada layout CSS responsivo, [01-develop-themes](../../../../PROJECTS/KEYCLOAK/DOCS/HOW-TO/01-develop-themes.md) guia desenvolvimento temas Keycloak, [05-theme-customization](../../../../PROJECTS/KEYCLOAK/DOCS/FEATURES/05-theme-customization.md) visão geral customização temas login account email, Keycloak Theme Configuration keycloak.org/docs/latest/server_admin/#_themes documentação oficial.
