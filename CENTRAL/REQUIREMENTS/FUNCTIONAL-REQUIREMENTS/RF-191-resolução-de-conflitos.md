---
modules: [GEOWEB, REURBCAD]
epic: audit
---

# RF-191: Resolução de Conflitos

O sistema fornece interface intuitiva de resolução de conflitos que apresenta ao usuário tela dedicada exibindo registros em conflito identificados durante sincronização, onde cada conflito é mostrado com visualização diff visual que destaca campos modificados em cada versão divergente utilizando cores diferenciadas para facilitar identificação rápida de diferenças. Para cada conflito, o usuário dispõe de três opções de resolução claramente apresentadas através de botões de ação, incluindo Manter local que descarta versão do servidor e persiste modificações locais como versão definitiva, Manter servidor que descarta edições locais e aceita versão do servidor como verdadeira, ou Mesclar que permite combinar seletivamente atributos de ambas as versões escolhendo campo por campo qual valor deve ser preservado. A interface de mesclagem apresenta formulário interativo onde cada campo conflitante exibe ambos os valores (local e servidor) com radio buttons ou checkboxes permitindo seleção granular de quais valores devem compor versão final mesclada, além de campo de texto livre para justificar decisão de resolução que será registrada em log de auditoria. Após resolução de todos os conflitos, o sistema persiste decisões tomadas e marca registros como sincronizados, permitindo que sincronizações subsequentes procedam normalmente sem reapresentação de conflitos já resolvidos.

---

**Última atualização:** 2025-12-30
