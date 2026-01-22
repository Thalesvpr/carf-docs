---
type: leaf
status: review
updated: 2026-01-21
---

# Desenvolvimento de Temas com Keycloakify

Este guia cobre o fluxo completo de desenvolvimento de temas Keycloak usando Keycloakify, desde a configuração inicial do ambiente até o deploy em produção.

## Pré-requisitos

Antes de iniciar o desenvolvimento, certifique-se de ter as seguintes ferramentas instaladas.

Node.js versão 18 ou superior é necessário para executar o Keycloakify CLI e o ambiente de desenvolvimento. Recomenda-se usar a versão LTS mais recente.

Um gerenciador de pacotes npm, yarn ou pnpm pode ser usado. O projeto CARF padroniza em pnpm para consistência com outros projetos do monorepo.

Docker é necessário para testes locais com uma instância Keycloak real. A imagem oficial quay.io/keycloak/keycloak será usada.

Conhecimento básico de React e TypeScript é assumido, já que os temas são desenvolvidos como aplicações React convencionais.

## Estrutura do Projeto

O projeto carf-keycloak-theme segue a estrutura padrão recomendada pelo Keycloakify com algumas adaptações para o contexto CARF.

O diretório raiz contém os arquivos de configuração: package.json com dependências e scripts, keycloakify.config.ts com configurações do tema, tsconfig.json para TypeScript, e vite.config.ts para o bundler.

O diretório src contém o código-fonte React. Dentro dele, o subdiretório login contém as páginas de autenticação (Login, Register, etc.), o subdiretório account contém as páginas do console de conta, e o subdiretório email contém os templates de email se customizados.

O diretório public contém assets estáticos como imagens, fontes e o favicon que serão incluídos no tema final.

Após o build, o diretório dist_keycloak é criado contendo o JAR do tema pronto para implantação.

## Configuração Inicial

Para criar um novo tema ou configurar o existente, algumas etapas são necessárias.

O arquivo keycloakify.config.ts é o ponto central de configuração. Nele define-se o nome do tema que aparecerá no Admin Console do Keycloak, as versões do Keycloak suportadas, propriedades extras do tema (equivalentes ao theme.properties), e configurações de build como diretório de saída.

As propriedades do tema definidas neste arquivo são acessíveis em runtime via kcContext.properties, permitindo configurar valores como URL do logo, cores primárias e informações de contato sem alterar o código.

A integração com @carf/ui requer que a biblioteca esteja disponível como dependência. No contexto do monorepo CARF, isso é feito via workspace reference. Em projetos standalone, a biblioteca deve ser instalada do registro npm.

## Ambiente de Desenvolvimento

O ambiente de desenvolvimento local permite iterar rapidamente sem precisar rebuildar o tema a cada mudança.

O comando de desenvolvimento inicia um servidor Vite com hot reload. As páginas do tema são renderizadas usando dados mock que simulam o contexto do Keycloak. Isso permite desenvolver e estilizar páginas sem uma instância Keycloak rodando.

Os mocks estão configurados para representar cenários comuns: login com erro, login bem-sucedido, registro com campos obrigatórios, recuperação de senha, etc. Cada cenário pode ser acessado via diferentes rotas do servidor de desenvolvimento.

Para testar cenários específicos não cobertos pelos mocks padrão, é possível criar mocks customizados que representem situações como login social, autenticação em dois fatores, ou erros específicos de validação.

## Customização de Páginas

Cada página do fluxo de autenticação pode ser customizada independentemente.

A página de login é o ponto de entrada mais comum e geralmente a primeira a ser customizada. Ela deve exibir o formulário de credenciais, opções de login social se configuradas, links para registro e recuperação de senha, e mensagens de erro quando aplicável.

A página de registro apresenta o formulário de criação de conta. Os campos exibidos dependem da configuração do realm no Keycloak. O tema deve renderizar dinamicamente os campos configurados, respeitando quais são obrigatórios e quais são opcionais.

A página de erro é exibida quando algo dá errado no fluxo de autenticação. Ela deve apresentar a mensagem de erro de forma clara e oferecer opções para o usuário (tentar novamente, voltar ao login, etc.).

Para customizar uma página, cria-se um componente React que recebe o kcContext específico daquela página como prop. O componente tem acesso a todas as informações necessárias via este contexto, incluindo URLs de ação do formulário, mensagens i18n, dados do usuário e configurações do realm.

## Internacionalização

O sistema de i18n do Keycloakify integra-se com o mecanismo de mensagens do Keycloak.

As mensagens padrão do Keycloak estão disponíveis via função msg() que recebe a chave da mensagem e retorna o texto no idioma atual do usuário. As chaves são as mesmas usadas em templates FreeMarker e documentadas na referência do Keycloak.

Mensagens customizadas podem ser adicionadas criando arquivos de mensagens no diretório apropriado. O formato segue o padrão Java properties com chave=valor. Arquivos separados são criados para cada idioma suportado (messages_pt_BR.properties, messages_en.properties, etc.).

O idioma atual é determinado pelo Keycloak baseado nas configurações do realm e preferências do usuário. O tema pode oferecer um seletor de idioma se o realm tiver internacionalização habilitada com múltiplos idiomas.

## Estilização

A estilização do tema utiliza as ferramentas padrão do ecossistema React.

Os tokens do Design System CARF (cores, tipografia, espaçamento) devem ser usados para garantir consistência visual. Esses tokens estão disponíveis como variáveis CSS quando @carf/ui é importado.

O Tailwind CSS pode ser usado para estilização utilitária, seguindo o mesmo padrão das aplicações CARF. A configuração do Tailwind deve estender o preset @carf/ui que define as cores e breakpoints institucionais.

Estilos específicos do tema que não se encaixam em classes utilitárias podem ser escritos em arquivos CSS separados ou usando a abordagem de módulos CSS para escopo local.

## Testes Locais com Keycloak

Para validar o tema em uma instância Keycloak real, um ambiente Docker é disponibilizado.

O arquivo docker-compose.dev.yml na raiz do projeto configura uma instância Keycloak com o tema montado como volume. Mudanças nos arquivos fonte são refletidas após reload da página, sem necessidade de restart do container.

O realm de desenvolvimento já vem configurado com um client de teste, usuários de exemplo e todas as features habilitadas (registro, recuperação de senha, login social mock) para facilitar testes de todos os fluxos.

Para testar fluxos específicos como verificação de email ou reset de senha, o maildev é incluído no docker-compose como servidor SMTP fake, permitindo visualizar os emails enviados pelo Keycloak.

## Build de Produção

O build de produção gera o artefato final para implantação.

O comando de build executa a compilação TypeScript, bundling via Vite, otimização de assets e empacotamento em JAR. O processo completo é automatizado pelo Keycloakify CLI.

O JAR resultante contém o tema compilado no formato esperado pelo Keycloak: diretórios de recursos, templates HTML gerados e arquivo theme.properties. Este JAR é idêntico em estrutura a um tema FreeMarker tradicional.

Validação pós-build deve incluir verificação do tamanho do bundle (alertar se exceder limites definidos), checagem de assets incluídos e teste de carregamento em instância Keycloak limpa.

## Deploy

O deploy do tema em ambientes Keycloak pode seguir diferentes estratégias.

Para **Keycloak em container**, o JAR deve ser copiado para o diretório /opt/keycloak/providers/ dentro do container. Isso pode ser feito via volume mount ou incluindo o JAR em uma imagem derivada da imagem base do Keycloak.

Para **Keycloak standalone**, o JAR é copiado para o diretório providers/ da instalação. Após copiar, é necessário executar o comando de build do Keycloak para registrar o novo provider.

Após o deploy, o tema fica disponível para seleção no Admin Console do Keycloak. Navegue até Realm Settings > Themes e selecione o tema carf nos dropdowns de Login theme, Account theme e Email theme conforme apropriado.

## Pipeline CI/CD

A integração com pipelines de CI/CD automatiza o build e deploy do tema.

O stage de build deve instalar dependências, executar linting e testes, buildar o tema e armazenar o JAR como artefato do pipeline.

O stage de deploy copia o JAR para o ambiente alvo. Em ambientes Kubernetes, isso geralmente envolve atualizar um ConfigMap ou Secret que é montado no pod do Keycloak, seguido de rolling restart.

Testes de smoke pós-deploy devem verificar que o tema carrega corretamente acessando a página de login e verificando elementos visuais esperados.

## Troubleshooting

Problemas comuns durante o desenvolvimento e suas soluções.

Se as **mudanças não aparecem**, verifique se o cache de temas está desabilitado no Keycloak de desenvolvimento. As variáveis KC_SPI_THEME_CACHE_THEMES e KC_SPI_THEME_CACHE_TEMPLATES devem ser false.

Se o **build falha**, verifique a versão do Node.js (deve ser 18+) e se todas as dependências estão instaladas. Limpe o diretório node_modules e reinstale se necessário.

Se o **tema não aparece** no Admin Console após deploy, verifique os logs do Keycloak durante startup para erros de carregamento de providers. O JAR deve estar no diretório correto e o Keycloak deve ter sido reiniciado após a adição.

Se há **erros de runtime**, verifique o console do browser para erros JavaScript. Problemas comuns incluem acesso a propriedades undefined do kcContext (verifique tipos) e imports incorretos de componentes.

## Referencias

Para detalhes sobre as APIs e tipos disponiveis, consulte [REFERENCE/04-keycloakify-api.md](../REFERENCE/04-keycloakify-api.md).

Para entender os conceitos por tras do Keycloakify, consulte [CONCEPTS/01-keycloak-themes.md](../CONCEPTS/01-keycloak-themes.md).

A documentacao oficial do Keycloakify em keycloakify.dev contem guias adicionais e exemplos de temas da comunidade.
