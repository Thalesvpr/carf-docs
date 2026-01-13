---
modules: [GEOWEB, GEOGIS]
epic: compatibility
---

# RF-212: Adicionar Camada WMS

O sistema permite que usuários com perfil ADMIN adicionem dinamicamente camadas WMS (Web Map Service) externas ao mapa interativo, possibilitando integração de bases cartográficas oficiais disponibilizadas por órgãos governamentais ou instituições especializadas sem necessidade de download ou armazenamento local de dados. A interface de configuração solicita URL do servidor WMS e executa automaticamente requisição GetCapabilities que recupera metadados do serviço incluindo lista de layers disponíveis, sistemas de coordenadas suportados, extensão espacial coberta e formatos de imagem oferecidos, apresentando essas informações em interface de seleção que permite ao administrador escolher quais layers específicos devem ser adicionados ao catálogo do sistema. Para cada camada adicionada, o sistema permite configurar parâmetros de exibição incluindo opacidade que controla transparência para permitir sobreposição legível com outras camadas, ordem ou z-index que define se camada aparece acima ou abaixo de outras features no mapa, nome amigável exibido aos usuários finais, e opcionalmente restrições de visibilidade por role que limitam acesso a camadas sensíveis. As camadas WMS configuradas ficam disponíveis no seletor de camadas do mapa para todos os usuários autorizados, que podem ativar ou desativar visualização conforme necessidade durante análises espaciais, enriquecendo contexto cartográfico com informações complementares como limites administrativos, hidrografia, imagens de satélite, zoneamento urbano ou qualquer outro dado geoespacial disponibilizado através de serviços OGC padrão.

---

**Última atualização:** 2025-12-30
