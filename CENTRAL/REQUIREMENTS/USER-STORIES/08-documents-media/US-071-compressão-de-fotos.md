---
modules: [GEOAPI]
epic: scalability
---

# US-071: Compressão de Fotos

Como sistema, quero comprimir automaticamente fotos antes de armazenar permanentemente no servidor para que otimização de storage seja garantida reduzindo custos de infraestrutura e melhorando performance de transferência, onde a funcionalidade deve redimensionar imagens automaticamente para resolução máxima de 1920x1080 pixels mantendo aspect ratio original, garantindo aplicação de compressão JPEG com qualidade de 85% balanceando tamanho de arquivo e qualidade visual, permitindo opcionalmente manutenção da imagem original em resolução completa para casos onde qualidade máxima seja necessária. Esta funcionalidade é implementada pelo módulo GEOAPI no backend utilizando bibliotecas de processamento de imagem (ImageSharp Sharp Pillow ou similar) executando compressão após upload e antes de armazenamento final, sem requisitos funcionais ou casos de uso específicos por ser otimização técnica transparente ao usuário. Os critérios de aceitação incluem detecção automática de imagens que excedem dimensões máximas de 1920x1080 pixels, redimensionamento proporcional mantendo aspect ratio original quando imagem for maior que limite, aplicação de compressão JPEG com fator de qualidade 85% (escala 0-100) para otimizar tamanho, preservação de metadados EXIF críticos (data geolocalização orientação) durante processo de compressão, geração de múltiplas versões incluindo thumbnail (200x200) versão comprimida (1920x1080 max) e opcionalmente original, armazenamento eficiente organizando versões em estrutura de diretórios ou blob storage com naming convention claro, processamento assíncrono de compressão através de job queue para não bloquear resposta de upload, monitoramento de redução de tamanho logando estatísticas de compressão (tamanho original versus comprimido), e configuração flexível permitindo ajustar parâmetros de qualidade e dimensões máximas via settings. A rastreabilidade não possui requisitos funcionais específicos, sendo implementação técnica para otimização de recursos de infraestrutura.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
