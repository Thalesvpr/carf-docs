# Theme Properties

Arquivo theme.properties na raiz de cada theme type (login/account/email) configura herança recursos e comportamento. Property parent define theme pai para herança (parent=keycloak.v2 herda base oficial), styles lista arquivos CSS carregados em ordem (styles=css/login.css css/custom.css), scripts lista JavaScript (scripts=js/validation.js js/cpf.js), locales define idiomas suportados (locales=pt-BR,en,es) com messages_pt-BR.properties contendo traduções. Import permite importar recursos de common theme (import=common/keycloak) compartilhando assets entre types. Cache properties cacheThemes=true e cacheTemplates=true habilitam caching em produção melhorando performance mas devem ser false em desenvolvimento para hot reload. Property kcHtmlClass define classe CSS no html tag, kcBodyClass no body permitindo styling global. Variáveis customizadas declaradas aqui ficam acessíveis nos templates FreeMarker via properties.nomeVariavel. Estrutura diretórios theme inclui resources/ para CSS JS imagens, messages/ para i18n properties, templates/ para .ftl FreeMarker overrides de páginas específicas login.ftl register.ftl error.ftl.

---

**Última atualização:** 2026-01-12
