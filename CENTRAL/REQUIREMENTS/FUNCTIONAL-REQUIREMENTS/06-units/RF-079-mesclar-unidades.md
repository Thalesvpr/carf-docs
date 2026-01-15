---
modules: [GEOWEB]
epic: units
---

# RF-079: Mesclar Unidades

O sistema deve permitir que administradores (perfil ADMIN) mesclem múltiplas unidades habitacionais em uma única unidade resultante, onde operação é útil para corrigir cadastros duplicados ou representar unificação física de edificações previamente separadas. A interface permite seleção de múltiplas unidades diretamente no mapa através de clique sequencial ou desenho de polígono envolvente, onde unidades selecionadas são destacadas visualmente e lista lateral apresenta resumo das unidades que serão mescladas. A geometria da unidade resultante é calculada através de união (ST_Union) das geometrias das unidades originais criando polígono único que engloba área total anteriormente ocupada pelas unidades separadas, garantindo preservação completa da extensão espacial. Titulares de todas as unidades originais são automaticamente vinculados à unidade mesclada preservando relacionamentos e evitando perda de informação sobre responsáveis, enquanto unidades originais são inativadas (soft delete) ao invés de excluídas permanentemente, mantendo rastreabilidade histórica da operação de mesclagem e permitindo eventual reversão se necessário através de restauração de registros inativados e exclusão da unidade mesclada.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
