---
modules: [GEOWEB]
epic: reliability
---

# RF-215: Listar Camadas WMS/WMTS

O sistema fornece interface administrativa de listagem que exibe todos os serviços WMS/WMTS configurados no sistema através de tabela estruturada contendo colunas essenciais como URL do servidor, nome amigável exibido aos usuários, tipo de serviço (WMS ou WMTS), layers consumidos, status de disponibilidade (ativo ou inativo) e data de última validação. A listagem implementa edição inline que permite administradores modificarem rapidamente atributos simples como nome de exibição ou opacidade padrão diretamente na tabela através de clique em campos editáveis, sem necessidade de navegar para formulário separado de edição, agilizando operações de manutenção rotineira e ajustes menores de configuração. Funcionalidade de ativação/desativação através de toggle switch permite administradores controlarem rapidamente visibilidade de camadas para usuários finais sem necessidade de excluir configuração permanentemente, sendo útil para desabilitar temporariamente serviços externos indisponíveis por manutenção ou substituir camadas obsoletas por versões atualizadas sem perder histórico de configuração. A interface oferece recursos adicionais de filtragem por tipo de serviço ou status, busca textual por nome ou URL, e ordenação por qualquer coluna, facilitando gestão de catálogos extensos com dezenas de camadas configuradas provenientes de múltiplas fontes externas incluindo órgãos governamentais, instituições de pesquisa e provedores comerciais de dados geoespaciais.

---

**Última atualização:** 2025-12-30
