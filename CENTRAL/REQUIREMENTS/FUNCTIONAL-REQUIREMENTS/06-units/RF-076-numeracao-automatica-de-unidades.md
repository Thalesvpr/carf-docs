---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: compatibility
---

# RF-076: Numeração Automática de Unidades

O sistema deve oferecer geração automática de códigos identificadores para unidades habitacionais seguindo padrão configurável por tenant, onde template de numeração pode incluir prefixos, códigos hierárquicos (comunidade-quadra-unidade) e contadores sequenciais resultando em códigos como C001-Q01-U001 que refletem estrutura territorial. A geração utiliza sequências de banco de dados garantindo unicidade mesmo em cenários de cadastramento concorrente por múltiplos usuários simultaneamente, onde transações isoladas previnem duplicações e garantem integridade referencial dos identificadores atribuídos. Usuários mantêm opção de override manual permitindo especificação de código customizado quando necessário, acomodando situações especiais como migração de cadastros legados, integração com sistemas externos ou adequação a nomenclaturas pré-existentes reconhecidas pela comunidade. Implementado no módulo GEOAPI com prioridade Could-have, este recurso otimiza produtividade em cadastramentos massivos eliminando necessidade de inventar códigos manualmente, reduzindo erros de digitação e duplicações, enquanto mantém flexibilidade para casos excepcionais através de possibilidade de especificação manual quando padrão automático não se aplica adequadamente.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
