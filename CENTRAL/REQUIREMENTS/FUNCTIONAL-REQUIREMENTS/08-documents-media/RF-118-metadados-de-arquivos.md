---
modules: [GEOWEB]
epic: compatibility
---

# RF-118: Metadados de Arquivos

Este requisito especifica que o sistema deve armazenar conjunto abrangente de metadados para cada arquivo documento ou foto gerenciado, onde metadados essenciais incluem nome original do arquivo preservando nomenclatura fornecida pelo usuário, tamanho em bytes permitindo monitoramento de storage, tipo MIME real do conteúdo validado durante upload, data e hora precisa de upload com timezone, e identificação do usuário que realizou upload para rastreabilidade. Os campos de metadados devem ser atualizados automaticamente durante processo de upload sem intervenção manual, onde sistema extrai informações diretamente do arquivo recebido e contexto da requisição, garantindo consistência e completude dos dados. A interface frontend deve exibir metadados de forma clara e organizada em telas de detalhes ou listagens expandidas, permitindo que usuários vejam informações completas sobre cada arquivo incluindo quem fez upload quando e características técnicas do arquivo. O sistema deve validar e normalizar metadados durante ingestão, convertendo tamanhos para formato legível, formatando datas adequadamente e preservando tipo MIME correto independente de extensão declarada. Os metadados devem ser indexados para permitir buscas eficientes por nome arquivo, tipo ou data. A funcionalidade deve ser implementada no módulo GEOAPI através de campos no modelo de dados e endpoints que retornam informações completas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
