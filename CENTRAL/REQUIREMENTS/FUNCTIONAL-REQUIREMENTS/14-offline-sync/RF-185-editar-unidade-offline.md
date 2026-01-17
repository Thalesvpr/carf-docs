---
modules: [GEOWEB, REURBCAD]
epic: units
---

# RF-185: Editar Unidade Offline

O sistema possibilita edição de unidades territoriais existentes no modo offline, permitindo que técnicos em campo atualizem informações cadastrais, corrijam dados imprecisos, complementem atributos incompletos ou ajustem geometrias espaciais conforme verificações in loco, tudo sem necessidade de conectividade. As edições realizadas são persistidas imediatamente no banco de dados local SQLite e a unidade modificada recebe marcação automática de alteração através de flag e timestamp que registram momento da edição, permitindo rastreamento posterior de quais registros foram modificados offline e precisam ser sincronizados com servidor. O sistema implementa mecanismo de detecção de conflitos que compara timestamp de última atualização da versão local com timestamp da versão no servidor durante sincronização subsequente, identificando situações onde o mesmo registro foi editado simultaneamente em diferentes dispositivos ou na interface web, permitindo tratamento apropriado dessas colisões. Enquanto não sincronizada, a versão editada offline permanece disponível localmente com indicação visual de pendência de sincronização, garantindo que usuário tenha consciência de quais alterações já foram efetivadas no sistema central e quais ainda aguardam transmissão quando conectividade for restabelecida.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
