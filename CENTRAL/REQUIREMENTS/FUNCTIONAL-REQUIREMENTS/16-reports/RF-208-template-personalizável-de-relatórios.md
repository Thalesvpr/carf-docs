---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: usability
---

# RF-208: Template Personalizável de Relatórios

O sistema oferece a usuários com perfil ADMIN capacidade de customizar templates de relatórios PDF através de editor visual que permite modificação de estrutura HTML e estilos CSS, possibilitando adaptação de layout, formatação e conteúdo de documentos gerados conforme identidade visual institucional, requisitos formais específicos ou preferências estéticas de cada organização. O editor implementa sistema de variáveis dinâmicas que podem ser inseridas no template através de sintaxe especial como {{unidade.codigo}}, {{titular.nome}} ou {{comunidade.area_total}}, sendo automaticamente substituídas por valores reais provenientes do banco de dados durante geração efetiva do relatório, permitindo criação de templates genéricos reutilizáveis que se adaptam a diferentes contextos de dados. A funcionalidade disponibiliza preview em tempo real que renderiza template sendo editado com dados de exemplo representativos, permitindo que administrador visualize aparência final do relatório antes de salvar template e disponibilizá-lo para uso em produção, reduzindo ciclos de tentativa e erro e garantindo qualidade do produto final. Templates customizados podem incluir elementos avançados como tabelas dinâmicas que iteram sobre coleções de dados, gráficos gerados a partir de bibliotecas JavaScript, códigos QR contendo URLs de acesso a registros específicos, e imagens de mapas estáticos mostrando localização de unidades, proporcionando flexibilidade máxima para criação de documentação técnica sofisticada adaptada a necessidades específicas de cada projeto de regularização fundiária.

---

**Última atualização:** 2025-12-30
