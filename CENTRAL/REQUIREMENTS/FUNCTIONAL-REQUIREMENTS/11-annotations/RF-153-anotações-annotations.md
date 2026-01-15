---
modules: [GEOWEB, REURBCAD]
epic: usability
---

# RF-153: Anotações (Annotations)

Este requisito estabelece que usuários devem poder criar anotações pontuais no mapa combinando localização geográfica com texto descritivo permitindo documentação de observações notas de campo ou marcações temporárias durante análise e planejamento, onde anotações são features especializadas com ênfase no conteúdo textual. O sistema deve permitir criação de anotação através de clique no mapa para definir ponto de localização seguido de entrada de texto onde usuário digita observação nota ou comentário em campo apropriado, criando registro que vincula coordenadas geográficas a conteúdo textual descritivo. As anotações devem ser renderizadas no mapa com ícone diferenciado que distingue visualmente de outros tipos de features usando símbolo específico como pin com balão de texto nota adesiva ou marcador colorido, garantindo que usuários identifiquem facilmente anotações entre outras informações espaciais. O sistema deve fornecer listagem de anotações em painel lateral ou interface separada apresentando todas as anotações do contexto atual ordenadas por data autor ou localização, onde lista permite navegação rápida e acesso a anotações sem necessidade de localizar visualmente cada uma no mapa, incluindo funcionalidade de zoom para anotação selecionada. Cada anotação deve armazenar metadados incluindo autor timestamp e opcionalmente categoria ou tag permitindo filtros e organização. A funcionalidade deve estar disponível nos módulos GEOWEB para criação e visualização e GEOAPI para persistência e listagem.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
