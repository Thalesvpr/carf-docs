---
modules: [REURBCAD]
epic: maintainability
---

# RF-186: Tirar Fotos Offline

O aplicativo mobile permite captura de fotos através da câmera do dispositivo sem necessidade de conectividade, funcionalidade essencial para documentação fotográfica de unidades territoriais durante levantamentos de campo em áreas sem cobertura de rede. A câmera funciona completamente offline utilizando recursos nativos do dispositivo, capturando imagens em resolução configurável que equilibra qualidade visual com tamanho de arquivo para otimizar uso de armazenamento local e posterior transmissão durante sincronização. As imagens capturadas são armazenadas localmente no sistema de arquivos do dispositivo com nomenclatura estruturada que inclui UUID da unidade associada e timestamp de captura, enquanto metadados como coordenadas GPS do local da foto, orientação da câmera e identificação do usuário são registrados no banco SQLite local, estabelecendo vínculo entre arquivo de imagem e registro cadastral correspondente. Durante próxima sincronização quando conectividade for restabelecida, o sistema realiza upload automático das fotos para servidor central através de processo otimizado que pode comprimir imagens, realizar uploads em background e retomar transferências interrompidas, garantindo que documentação fotográfica coletada em campo seja persistida de forma confiável no repositório central independentemente de instabilidades de conexão.

---

**Última atualização:** 2025-12-30
