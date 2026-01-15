---
modules: [GEOWEB, REURBCAD]
epic: reliability
---

# US-040: Cadastrar Unidade Offline

Como agente de campo, quero cadastrar unidade sem internet para que trabalho não seja interrompido, onde o sistema mobile implementa capacidades offline-first permitindo coleta de dados em áreas sem conectividade através de armazenamento local e sincronização posterior, garantindo produtividade contínua em campo independente de disponibilidade de rede. O cenário principal de uso ocorre quando agente de campo está em área sem cobertura de internet e precisa cadastrar unidade, onde aplicativo mobile permanece totalmente funcional permitindo preencher formulário completo, desenhar geometria usando GPS, e anexar fotos, com todos os dados sendo salvos localmente no dispositivo para posterior sincronização quando conectividade for restabelecida. Os critérios de aceitação incluem funcionamento completo do formulário offline onde todos os campos permanecem editáveis e validações client-side são executadas mesmo sem conexão com servidor, armazenamento de dados em WatermelonDB local que é banco de dados offline-first no dispositivo mobile persistindo informações de forma estruturada e confiável, marcação de registros com flag synced: false indicando que dados ainda não foram enviados ao servidor e precisam ser sincronizados quando possível, e sincronização automática quando online onde aplicativo detecta restabelecimento de conectividade e envia automaticamente dados pendentes para servidor sem intervenção manual. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoints de sincronização que recebem lotes de unidades criadas offline e processam com resolução de conflitos) e aplicativo mobile (armazenamento WatermelonDB, detecção de conectividade e serviço de sincronização em background), garantindo rastreabilidade com RF-182 (Cadastro Offline) e UC-004 (Caso de Uso de Coleta de Campo), onde conflitos entre dados offline e servidor são detectados e resolvidos, usuário recebe feedback claro sobre status de sincronização de cada registro, e dados permanecem seguros no dispositivo mesmo em caso de falha de app através de persistência durável em SQLite local.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Pronto
