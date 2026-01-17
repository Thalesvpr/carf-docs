---
modules: [GEOWEB, REURBCAD]
epic: other
---

# RF-182: Modo Offline (Mobile)

O aplicativo mobile funciona completamente offline permitindo coleta e gestão de dados cadastrais em campo mesmo sem conectividade com internet ou rede celular, requisito essencial para trabalho em comunidades remotas ou áreas com infraestrutura de telecomunicações precária. A implementação utiliza SQLite como banco de dados local através da biblioteca WatermelonDB que fornece camada de abstração reativa e performática, possibilitando armazenamento estruturado de milhares de registros de unidades territoriais, titulares, fotos e documentos diretamente no dispositivo móvel. Todas as funcionalidades principais do aplicativo permanecem disponíveis no modo offline incluindo criação e edição de unidades, cadastro de titulares, captura de fotos georeferenciadas, desenho de geometrias no mapa e preenchimento de formulários, garantindo que trabalho de campo não seja interrompido por ausência de conectividade. O sistema exibe indicador visual permanente de status de conectividade (online/offline) na interface, informando claramente ao usuário contexto atual de operação e alertando sobre necessidade futura de sincronização para que dados locais sejam persistidos no servidor central, promovendo consciência situacional e prevenindo perda de informações coletadas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
