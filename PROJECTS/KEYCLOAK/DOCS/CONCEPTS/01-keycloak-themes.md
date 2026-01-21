---
status: approved
updated: 2026-01-21
---

# Keycloak Themes

O sistema de temas do Keycloak permite customizar a aparência de todas as interfaces de usuario (login, registro, account console, emails). No projeto CARF, utilizamos **Keycloakify** como tecnologia padrao para desenvolvimento de temas, permitindo criar interfaces com React e TypeScript.

## O Que É Keycloakify

Keycloakify é um toolkit open-source que compila aplicações React em temas Keycloak compatíveis. O resultado final é um arquivo JAR que pode ser implantado em qualquer instância Keycloak, exatamente como um tema FreeMarker tradicional. A diferença está apenas no processo de desenvolvimento, não na implantação.

A ferramenta funciona como uma camada de abstração que traduz o contexto do Keycloak (variáveis FreeMarker, URLs, mensagens i18n) para props React acessíveis via TypeScript. Durante o build, a aplicação React é compilada para HTML estático que o Keycloak serve normalmente.

## Motivação para Adoção

A decisão de adotar Keycloakify no projeto CARF foi documentada em ADR-024 e fundamenta-se em três pilares principais.

O primeiro pilar é a **reutilização de componentes**. O projeto já possui a biblioteca @carf/ui com componentes React estilizados segundo o Design System institucional. Com Keycloakify, esses mesmos componentes (Button, Input, Card, Alert) podem ser usados nas telas de login, registro e recuperação de senha, garantindo consistência visual absoluta entre a aplicação principal e as telas de autenticação.

O segundo pilar é a **experiência de desenvolvimento**. Desenvolvedores já familiarizados com React e TypeScript podem criar e manter temas sem precisar aprender FreeMarker, uma tecnologia de template Java com sintaxe própria. Além disso, o hot reload funciona durante o desenvolvimento, permitindo ver mudanças instantaneamente.

O terceiro pilar é a **qualidade de código**. TypeScript fornece tipagem estática para todas as variáveis de contexto do Keycloak, eliminando erros de runtime causados por acessos a propriedades inexistentes. O sistema de tipos documenta automaticamente quais dados estão disponíveis em cada página.

## Comparação com FreeMarker

A tabela abaixo compara as duas abordagens de desenvolvimento de temas.

| Aspecto | FreeMarker | Keycloakify |
|:--------|:-----------|:------------|
| Linguagem | Template FreeMarker (.ftl) | React/TypeScript (.tsx) |
| Estilização | CSS puro ou SCSS | CSS, SCSS, Tailwind, CSS-in-JS |
| Componentização | Macros FreeMarker | Componentes React |
| Tipagem | Nenhuma | TypeScript completo |
| Hot Reload | Requer restart Keycloak | Funciona nativamente |
| Curva Aprendizado | Alta (sintaxe específica) | Baixa (se já conhece React) |
| Reutilização | Limitada ao tema | Qualquer componente React |
| Testes | Difícil | Jest, Testing Library |
| Bundle Final | Tema nativo | Tema nativo (idêntico) |

Do ponto de vista do Keycloak, não há diferença entre um tema FreeMarker e um tema Keycloakify após o build. Ambos resultam em arquivos HTML, CSS e JavaScript servidos da mesma forma.

## Arquitetura Keycloakify

O Keycloakify opera em três camadas distintas que trabalham juntas para produzir o tema final.

A **camada de contexto** (KcContext) é um objeto TypeScript que espelha todas as variáveis que o Keycloak disponibiliza para templates FreeMarker. Isso inclui informações do realm (nome, configurações de registro, políticas de senha), URLs de ação (login, logout, registro), dados do usuário tentando autenticar, mensagens de erro e sucesso, e configurações de internacionalização. Cada tipo de página (login, registro, erro, etc.) tem seu próprio tipo de contexto com as propriedades relevantes.

A **camada de páginas** contém os componentes React que renderizam cada tela do fluxo de autenticação. Keycloakify suporta todas as páginas padrão do Keycloak, incluindo login, registro, recuperação de senha, atualização de senha, verificação de email, seleção de identity provider, consentimento OAuth, erro e logout. Cada página recebe o KcContext apropriado e pode usar qualquer componente React.

A **camada de build** é responsável por transformar a aplicação React em um tema Keycloak válido. O processo compila o React para HTML estático, gera o arquivo theme.properties automaticamente, empacota tudo em um JAR e produz artefatos compatíveis com o sistema de temas do Keycloak.

## Páginas Suportadas

Keycloakify fornece tipos e contextos para todas as páginas do fluxo de autenticação Keycloak.

| Página | Descrição | Contexto Principal |
|:-------|:----------|:-------------------|
| login.ftl | Formulário de login | username, social providers |
| register.ftl | Formulário de registro | campos de registro, termos |
| login-reset-password.ftl | Solicitação de reset | username/email |
| login-update-password.ftl | Atualização de senha | requisitos de senha |
| login-verify-email.ftl | Verificação de email | instruções, link |
| login-otp.ftl | Entrada de OTP/2FA | tipo de OTP |
| login-idp-link-email.ftl | Link de IdP por email | provider info |
| error.ftl | Página de erro | mensagem de erro |
| info.ftl | Página informativa | mensagem info |
| logout-confirm.ftl | Confirmação logout | client info |

Além destas, Keycloakify suporta páginas do Account Console e Email templates, permitindo customização completa de toda a experiência do usuário.

## Integração com @carf/ui

A principal vantagem do Keycloakify para o projeto CARF é a capacidade de importar e usar componentes da biblioteca @carf/ui diretamente nas páginas de autenticação.

Os componentes de formulário (Input, Button, Checkbox, Select) são usados nos campos de login e registro, mantendo a mesma aparência e comportamento da aplicação principal. Os componentes de feedback (Alert, Toast) exibem mensagens de erro e sucesso com o mesmo estilo visual. Os componentes de layout (Card, Container) estruturam as páginas de forma consistente.

Esta integração elimina a duplicação de código CSS e garante que qualquer atualização no Design System se reflita automaticamente nas telas de autenticação.

## Fluxo de Desenvolvimento

O desenvolvimento de temas com Keycloakify segue um fluxo específico que difere do desenvolvimento FreeMarker tradicional.

O **ambiente de desenvolvimento** executa a aplicação React localmente com hot reload. Keycloakify fornece um mock do KcContext que simula os dados que o Keycloak enviaria, permitindo desenvolver e testar sem uma instância Keycloak rodando.

A **validação** pode ser feita conectando o ambiente de desenvolvimento a uma instância Keycloak real em modo dev, onde o tema é carregado dinamicamente. Isso permite testar fluxos completos de autenticação.

O **build de produção** compila a aplicação, otimiza assets e gera o JAR final. Este JAR é copiado para o diretório de providers do Keycloak ou montado como volume em containers.

## Limitações

Keycloakify tem algumas limitações que devem ser consideradas.

O **tamanho do bundle** tende a ser maior que temas FreeMarker puros devido ao runtime React incluído. Para a maioria dos casos isso não é problema, mas pode impactar o tempo de carregamento inicial em conexões muito lentas.

A **complexidade de build** é maior, exigindo Node.js e npm no pipeline de CI/CD além das ferramentas Java do Keycloak. O projeto precisa manter dois ambientes de build.

**Páginas customizadas** que não existem no Keycloak padrão (criadas via SPIs de autenticação) requerem configuração adicional para que o Keycloakify gere os tipos corretos.

A **curva de aprendizado** inicial existe para entender como o KcContext mapeia para as variáveis FreeMarker e como o sistema de i18n funciona no contexto React.

## Documentacao Relacionada

Para implementacao pratica, consulte o guia [HOW-TO/01-develop-themes.md](../HOW-TO/01-develop-themes.md) que cobre setup do ambiente, desenvolvimento de paginas e processo de build.

Para referencia de APIs e tipos, consulte [REFERENCE/04-keycloakify-api.md](../REFERENCE/04-keycloakify-api.md) que documenta o KcContext, hooks disponiveis e configuracoes do keycloakify.config.ts.


## Referências Externas

A documentação oficial do Keycloakify está disponível em keycloakify.dev e inclui guias de início rápido, exemplos de temas e referência de API. O repositório GitHub keycloakify/keycloakify contém o código-fonte e issues para troubleshooting.
