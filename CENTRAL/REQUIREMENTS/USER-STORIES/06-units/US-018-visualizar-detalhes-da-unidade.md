---
modules: [GEOAPI]
epic: compatibility
---

# US-018: Visualizar Detalhes da Unidade

Como analista, quero ver todos os dados de uma unidade para que eu tenha visão completa do cadastro, onde o sistema apresenta página dedicada consolidando todas as informações relacionadas a uma unidade específica incluindo dados descritivos, espaciais, relacionamentos e histórico, garantindo compreensão holística do registro. O cenário principal de uso ocorre quando um analista seleciona uma unidade na listagem ou busca e acessa a página de detalhes que carrega e apresenta de forma organizada todas as informações associadas àquela unidade, permitindo navegação entre seções relacionadas sem perder o contexto da unidade sendo visualizada. Os critérios de aceitação incluem exibição completa de dados básicos como code (código identificador), type (tipo de unidade), área calculada em metros quadrados, status atual e datas de criação e última modificação, apresentação da geometria espacial em formato GeoJSON tanto como texto estruturado quanto visualizada em mapa interativo onde o polígono da unidade é destacado, listagem de holders vinculados mostrando titulares associados com seus respectivos tipos de relacionamento e percentuais de propriedade, galeria de documentos e fotos anexados permitindo visualização inline de imagens e download de documentos, e timeline completa de alterações apresentando histórico cronológico de todas as modificações feitas na unidade incluindo quem, quando e o que foi alterado. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint GET /api/units/{id} retornando objeto completo com relacionamentos incluídos via eager loading) e GEOWEB (página de detalhes com layout em tabs ou seções colapsáveis organizando as diferentes categorias de informação), garantindo rastreabilidade com RF-053 (Visualização de Detalhes de Unidade) e UC-001 (Caso de Uso de Gestão de Unidades), onde informações sensíveis são filtradas baseadas em permissões do usuário e links de navegação permitem acesso rápido a entidades relacionadas como comunidade ou titulares.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Pronto
