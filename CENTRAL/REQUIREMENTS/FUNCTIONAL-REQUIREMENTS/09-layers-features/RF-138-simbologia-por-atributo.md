---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: performance
---

# RF-138: Simbologia por Atributo

Este requisito especifica que o sistema deve suportar aplicação de estilos visuais diferentes a features da mesma camada baseado em valores de seus atributos permitindo visualização temática e categorização visual de dados geoespaciais, onde regras de estilo condicionais determinam aparência de cada feature conforme suas propriedades. O sistema deve permitir definição de regras de estilo usando sintaxe condicional tipo if attribute equals X then color equals Y, onde administrador configura mapeamento entre valores de atributo específico e estilos correspondentes, permitindo criar mapas coropléticos ou categorizados automaticamente. A funcionalidade deve suportar categorização tanto para valores discretos quanto contínuos, onde valores discretos como tipos ou categorias mapeiam para cores distintas através de correspondência exata, e valores numéricos contínuos são divididos em ranges com estilos graduados criando representação de intensidade ou densidade. O sistema deve gerar legendas automáticas baseadas nas regras de estilo configuradas mostrando mapeamento visual entre categorias ou ranges de valores e suas cores ou símbolos correspondentes, onde legenda é exibida no painel do mapa permitindo que usuários interpretem corretamente a visualização temática. A configuração de simbologia por atributo deve ser armazenada como parte da definição da camada e aplicada dinamicamente durante renderização. A funcionalidade deve estar disponível nos módulos GEOWEB para visualização e GEOAPI para configuração.

---

**Última atualização:** 2025-12-30