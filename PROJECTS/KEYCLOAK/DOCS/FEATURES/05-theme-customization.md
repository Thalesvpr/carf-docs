---
type: leaf
status: review
updated: 2026-02-08
---

# Theme Customization

O tema CARF customiza a identidade visual das paginas de autenticacao, gerenciamento de conta e emails transacionais do Keycloak. A implementacao usa templates FreeMarker com CSS customizado, deployada em /opt/keycloak/themes/carf/ na imagem Docker.

## Estrutura de Diretorios

O tema reside em PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/themes/carf/ com tres subdiretorios, cada um contendo theme.properties que define heranca do tema pai, templates .ftl que sobreescrevem o comportamento padrao, resources/ com CSS, JavaScript e imagens, e messages/ com traducoes.

O subdirectorio login/ contem o tema de login com layout split-screen, formularios customizados e validacao CPF. Herda de keycloak base.

O subdirectorio account/ contem o tema de gerenciamento de conta com customizacao visual. Herda de keycloak.v2.

O subdirectorio email/ contem templates HTML e texto puro para emails transacionais com branding CARF.

## Customizacao Visual

As cores institucionais sao definidas via CSS custom properties no login.css (437 linhas). Verde primario #2C5F2D para branding, botoes e links. Verde secundario #97BC62 para gradientes e destaques. Vermelho #dc2626 para alertas de erro. Cinza claro #f9fafb para background. Preto #111827 para textos.

A tipografia usa font-family Inter, Segoe UI, sans-serif como stack. Border-radius padrao 0.5rem para inputs e botoes. Inputs tem border 1px solid com focus outline na cor primaria e shadow-sm com transicao suave. Botoes primarios tem background na cor primaria, texto branco, hover 10% mais escuro, disabled opacity 50%.

O layout e responsivo com media query em max-width 768px para mobile e tablets, convertendo o split-screen em stack vertical e ajustando padding, margins e font-sizes.

## Templates FreeMarker

Seis templates sobreescritos no tema de login. O template.ftl define o layout base split-screen com painel esquerdo 42% (fundo verde, logo CARF, tagline "Sistema de Regularizacao Fundiaria Urbana") e painel direito 58% (area de formulario). O login.ftl renderiza campos CPF/email e senha com checkbox "lembrar-me". O register.ftl adiciona campos firstName, lastName, CPF e telefone mapeados como user attributes do Keycloak. O login-reset-password.ftl exibe formulario de recuperacao de senha por email. O error.ftl mostra mensagens de erro amigaveis em portugues com instrucoes de troubleshooting. O info.ftl exibe mensagens informativas.

## Validacao CPF

O login.js (337 linhas) registra window.CarfValidations com mascara automatica XXX.XXX.XXX-XX nos campos CPF e validacao dos digitos verificadores via algoritmo Mod11 no evento blur. O carf-validations.js e um bundle minificado complementar carregado via tag script no template.ftl.

## Internacionalizacao

Traducoes em messages_pt_BR.properties (334 chaves) como idioma principal e messages_en.properties (40 chaves) como secundario. Chaves customizadas incluem loginAccountTitle "Entrar no Sistema CARF", usernameOrEmail "CPF ou E-mail", password "Senha", doLogIn "Entrar", registerTitle "Cadastrar Nova Conta" e invalidUsernameOrEmailMessage "CPF ou e-mail invalido".

## Deploy

Em desenvolvimento, docker-compose.dev.yml monta themes/carf/ como volume bind com cache de tema desabilitado, permitindo hot reload de alteracoes em templates e CSS sem restart do container. Em producao, o Dockerfile multi-stage copia themes/ para /opt/keycloak/themes/carf/ na imagem final. Ativacao no Admin Console em Realm Settings, Themes, selecionando "carf" para Login Theme, Account Theme e Email Theme.

## Emails Transacionais

Templates HTML e texto puro em email/html/ e email/text/ para email-verification.ftl (verificacao de email com link de confirmacao) e password-reset.ftl (reset de senha com link temporario). Ambos usam header com gradiente verde (#2C5F2D a #97BC62), logo CARF e botao CTA na cor primaria.
