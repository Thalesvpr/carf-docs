---
modules: [GEOWEB, REURBCAD]
epic: communities
---

# RF-183: Download Inicial de Dados

O sistema possibilita download inicial de dados de comunidade específica para dispositivo móvel antes de deslocamento a campo, permitindo que usuário selecione comunidade de interesse através de interface intuitiva e baixe todos os dados associados incluindo unidades territoriais já cadastradas, titulares vinculados, fotos existentes, documentos anexados e configurações específicas da comunidade. O processo de download é implementado de forma otimizada que agrupa múltiplas requisições em lotes e comprime dados transmitidos, minimizando tempo de transferência e consumo de dados móveis, aspectos críticos considerando limitações de infraestrutura em muitas localidades. Durante execução, o sistema exibe barra de progresso detalhada que informa usuário sobre andamento do download incluindo percentual concluído, quantidade de registros já transferidos e estimativa de tempo restante, proporcionando feedback tranquilizador durante operação que pode levar vários minutos dependendo de volume de dados e qualidade da conexão. Ao concluir download, dados são persistidos no banco local SQLite e imediatamente disponibilizados para acesso offline, permitindo que usuário inicie trabalho de campo imediatamente após chegada à comunidade sem necessidade de conectividade adicional para consultar informações existentes ou criar novos registros.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
