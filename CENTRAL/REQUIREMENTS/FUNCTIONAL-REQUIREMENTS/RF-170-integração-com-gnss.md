---
modules: [REURBCAD]
epic: compatibility
---

# RF-170: Integração com GNSS

O sistema possibilita importação de dados coletados por receptores GNSS (Global Navigation Satellite System) e GPS através de parsers especializados que interpretam formatos padrão da indústria incluindo RINEX (Receiver Independent Exchange Format) para dados brutos de observação satelital e NMEA 0183 para sentenças de posicionamento em tempo real. A funcionalidade implementa opcionalmente processamento de correção diferencial que utiliza dados de estações de referência para refinar coordenadas obtidas, melhorando precisão posicional de nível métrico para submétrico ou centimétrico conforme método de processamento aplicado, seja pós-processado ou RTK (Real-Time Kinematic). Após importação e processamento, o sistema cria automaticamente pontos georreferenciados no banco de dados espacial, associando metadados de qualidade como PDOP (Position Dilution of Precision), número de satélites utilizados e tipo de solução obtida, permitindo rastreabilidade da precisão esperada para cada vértice cadastrado. Esta capacidade de integração com tecnologia GNSS é fundamental em projetos de regularização fundiária que demandam georreferenciamento preciso de limites territoriais conforme normas técnicas brasileiras, facilitando conformidade com requisitos do INCRA para certificação de imóveis rurais e urbanos.

---

**Última atualização:** 2025-12-30
