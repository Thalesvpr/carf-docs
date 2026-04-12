---
type: leaf
status: approved
updated: 2026-02-07
---

# Build and Release

Configuracao completa de build, distribuicao e release do aplicativo REURBCAD para Android e iOS usando EAS (Expo Application Services) como infraestrutura de build na nuvem.

## Variaveis de Ambiente

O app depende de cinco variaveis de ambiente, todas prefixadas com EXPO_PUBLIC para exposicao no bundle JavaScript apos build. EXPO_PUBLIC_KEYCLOAK_URL contem a URL base do servidor Keycloak (por exemplo https://auth.carf.gov.br). EXPO_PUBLIC_KEYCLOAK_REALM contem o nome do realm configurado para o CARF (por exemplo carf). EXPO_PUBLIC_KEYCLOAK_CLIENT_ID contem o client ID do Keycloak configurado como public client com PKCE para mobile (por exemplo reurbcad-mobile). EXPO_PUBLIC_API_URL contem a URL base da GEOAPI (por exemplo https://api.carf.gov.br). EXPO_PUBLIC_DEEP_LINK_SCHEME contem o scheme customizado para callbacks OAuth2 (por exemplo reurbcad).

Essas variaveis sao definidas no arquivo eas.json em cada profile de build, permitindo valores diferentes por ambiente. O ambiente de development aponta para Keycloak e API locais, preview aponta para o ambiente de homologacao, e production aponta para os servicos de producao.

## Profiles de Build

O EAS Build esta configurado com tres profiles no arquivo eas.json.

O profile development gera builds com Expo Dev Client habilitado, permitindo hot reload e debugging em dispositivos fisicos durante desenvolvimento. Usa certificados de debug auto-gerados. Variaveis apontam para servicos locais ou de desenvolvimento.

O profile preview gera builds para distribuicao interna via QR code. Incluem toda a funcionalidade de producao mas apontam para o ambiente de homologacao. Distribuidos via EAS Update para o canal preview, acessiveis sem publicar nas stores.

O profile production gera builds assinados para submissao nas stores. Keystore Android gerenciado pelo EAS (armazenado nos servidores do Expo de forma criptografada, nunca no repositorio). Provisioning iOS via Apple Developer account com perfil de distribuicao App Store.

## Versionamento

O versionamento segue o padrao MAJOR.MINOR.PATCH definido no campo version do arquivo app.json (ou app.config.js). MAJOR incrementa quando ha mudancas que quebram compatibilidade com dados locais do WatermelonDB (schema migration obrigatoria). MINOR incrementa a cada release com novas funcionalidades. PATCH incrementa para correcoes de bugs.

O build number (versionCode no Android e buildNumber no iOS) e auto-incrementado pelo EAS a cada build, sem necessidade de gerenciamento manual. Isso garante que cada build submetido para as stores tenha um numero unico crescente.

## Fluxo de Teste Interno

O fluxo de teste interno segue quatro passos. Primeiro, o desenvolvedor faz push para branch feature/* e abre pull request. Segundo, GitHub Actions executa lint, typecheck e testes unitarios. Terceiro, merge para branch develop dispara build automatico do profile preview via EAS Build. Quarto, testadores acessam a build via TestFlight (iOS, requer convite por email) e Google Play Internal Track (Android, requer conta no grupo de teste).

Para atualizacoes menores que nao envolvem mudancas em codigo nativo (apenas JavaScript), EAS Update publica atualizacao OTA (over-the-air) no canal preview, disponivel em ate 5 minutos sem necessidade de novo build.

## Checklist de Release para Producao

Antes de cada release para as stores, a equipe deve verificar todos os itens. Testar modo offline completo: desabilitar conexao de rede, criar unidade, cadastrar titular, vincular titular, tirar foto, coletar assinatura e verificar que tudo persiste localmente. Testar sincronizacao com conflitos simulados: editar mesma unidade em dois dispositivos offline, conectar ambos e verificar que conflito e detectado e resolvido. Testar permissoes de cada role: logar como coordenador e verificar acesso ao dashboard e lista de equipe, logar como cadastrador e verificar que dashboard e equipe estao ocultos. Testar cada status de atendimento: registrar unidade como ausente (verifica foto obrigatoria), presente (formulario completo), nao quis (observacao obrigatoria) e assinado (verifica assinatura). Testar fluxo OCR: escanear CNH e RG, verificar campos pre-preenchidos, verificar fallback para preenchimento manual.

## CI/CD

GitHub Actions configurado com dois workflows. O workflow de CI executa em cada push para qualquer branch: instala dependencias, executa lint (eslint), typecheck (tsc --noEmit), testes unitarios (jest) e verifica que o schema do WatermelonDB esta consistente com as migrations.

O workflow de release executa quando push e feito para branch release/*. Executa todos os passos do CI, depois dispara EAS Build para o profile production via eas-cli. Apos build bem-sucedido, submete automaticamente para App Store Connect (iOS) e Google Play Console (Android) via eas submit. A publicacao efetiva nas stores requer aprovacao manual no painel de cada store.
