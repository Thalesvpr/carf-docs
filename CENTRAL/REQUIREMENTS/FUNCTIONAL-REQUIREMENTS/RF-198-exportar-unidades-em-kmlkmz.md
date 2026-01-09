---
modules: [GEOWEB]
epic: compatibility
---

# RF-198: Exportar Unidades em KML/KMZ

O sistema possibilita exportação de unidades territoriais em formato KML (Keyhole Markup Language) ou sua versão compactada KMZ, padrão adotado pelo Google Earth que permite visualização tridimensional de dados geoespaciais em interface amigável acessível a usuários não técnicos. A geração de KML estrutura dados conforme especificação OGC incluindo elementos Placemark para cada unidade com geometrias codificadas em coordenadas WGS84 longitude/latitude, atributos alfanuméricos apresentados em popups HTML formatados, e metadados de estilo que definem cores, espessuras de linha e transparências para visualização adequada. O sistema aplica estilos diferenciados automaticamente conforme atributos das unidades como status (aprovado em verde, pendente em amarelo, rejeitado em vermelho) ou tipo de ocupação, facilitando interpretação visual imediata de características das features sem necessidade de consultar tabela de atributos. A opção de compactação em KMZ utiliza compressão ZIP para reduzir tamanho do arquivo resultante, particularmente benéfico quando exportação inclui grande quantidade de unidades ou quando arquivos serão distribuídos via email ou internet, garantindo transferências mais rápidas e consumo reduzido de armazenamento sem perda de informação ou qualidade dos dados espaciais.

---

**Última atualização:** 2025-12-30
