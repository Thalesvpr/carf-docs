---
modules: [GEOWEB, REURBCAD]
epic: reports
---

# RF-202: Exportar com Fotos/Documentos

O sistema disponibiliza opção avançada de exportação que inclui não apenas dados tabulares ou geoespaciais das unidades, mas também todos os arquivos de fotos e documentos vinculados, produzindo pacote completo em formato ZIP com estrutura de pastas organizada hierarquicamente. A estrutura de diretórios reflete organização lógica dos dados, criando pasta para cada unidade identificada por código cadastral, dentro da qual são colocadas subpastas separadas para fotos e documentos, com arquivos nomeados descritivamente incluindo timestamps e tipos, facilitando navegação manual e processamento automatizado. Arquivo CSV de metadados é incluído no ZIP descrevendo mapeamento entre unidades e arquivos correspondentes, listando caminhos relativos, tipos de arquivo, datas de upload, autores responsáveis e outros atributos que permitem processamento programático do pacote exportado ou reconstrução de vinculações em sistemas externos. Quando volume de dados a exportar é muito grande (milhares de unidades com múltiplas fotos cada), o sistema implementa geração assíncrona em background que processa exportação sem bloquear interface do usuário, enviando notificação por email ou in-app quando arquivo estiver pronto para download, evitando timeouts de navegador e proporcionando experiência adequada mesmo para exportações massivas que podem levar vários minutos para concluir.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
