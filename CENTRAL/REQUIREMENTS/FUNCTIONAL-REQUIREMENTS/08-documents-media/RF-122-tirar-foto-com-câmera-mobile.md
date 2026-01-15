---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: security
---

# RF-122: Tirar Foto com Câmera (Mobile)

Este requisito especifica que aplicativo mobile REURBCAD deve permitir que usuários capturem fotos diretamente através da câmera nativa do dispositivo durante trabalho de campo, onde funcionalidade acessa hardware de câmera do smartphone ou tablet através de APIs nativas do sistema operacional iOS ou Android. O sistema deve solicitar permissões apropriadas para acessar câmera conforme políticas de privacidade de cada plataforma, onde usuário concede acesso uma vez e app mantém permissão para usos futuros, implementando fluxo de autorização conforme guidelines oficiais. A interface de captura deve utilizar componente nativo de câmera fornecendo controles familiares ao usuário incluindo foco automático flash ajuste de exposição e preview em tempo real da imagem que será capturada. Após captura, o sistema deve oferecer opção de upload imediato se conectividade está disponível enviando foto diretamente para backend via API, ou armazenamento offline em storage local do dispositivo se conexão não está presente, onde fotos armazenadas localmente são sincronizadas automaticamente quando conectividade for restabelecida. O app deve preservar metadados EXIF incluindo coordenadas GPS se localização está habilitada, garantindo geotagging automático das fotos de campo. A funcionalidade é implementada exclusivamente no módulo REURBCAD mobile.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
