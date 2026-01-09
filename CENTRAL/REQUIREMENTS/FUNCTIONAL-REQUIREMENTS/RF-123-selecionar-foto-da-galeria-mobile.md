---
modules: [GEOWEB, REURBCAD]
epic: security
---

# RF-123: Selecionar Foto da Galeria (Mobile)

Este requisito estabelece que aplicativo mobile REURBCAD deve permitir que usuários selecionem fotos existentes da galeria do dispositivo ao invés de capturar novas através da câmera, onde funcionalidade acessa biblioteca de fotos através de APIs nativas de cada plataforma iOS ou Android. O sistema deve solicitar permissões de acesso à galeria de fotos conforme políticas de privacidade, onde usuário autoriza acesso e app pode subsequentemente navegar pela biblioteca disponível no dispositivo. A interface de seleção deve utilizar picker nativo familiar ao usuário permitindo navegação por álbuns e pastas do dispositivo, onde usuário pode visualizar thumbnails e selecionar uma ou múltiplas fotos conforme necessidade. O sistema deve suportar seleção múltipla permitindo que usuários escolham várias fotos simultaneamente através de interface multi-select com checkboxes ou gestos apropriados, facilitando upload em lote de documentação fotográfica coletada previamente. Após seleção, o sistema deve processar upload em lote de todas as fotos selecionadas, onde processo pode ocorrer imediatamente se há conectividade ou ser enfileirado para sincronização posterior se offline, mostrando progresso individual de cada upload e indicando sucessos ou falhas. A funcionalidade é implementada exclusivamente no módulo REURBCAD mobile.

---

**Última atualização:** 2025-12-30