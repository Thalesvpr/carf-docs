---
modules: [GEOAPI, GEOWEB]
epic: security
---

# RF-102: Upload de Documentos

O sistema deve permitir que usuários façam upload de documentos em formatos diversos (PDF DOCX XLSX JPG PNG) através de interface drag-and-drop ou seleção tradicional de arquivos, onde cada documento pode ser vinculado a diferentes entidades do sistema como unidades, titulares ou comunidades conforme contexto de uso. A validação de upload verifica formato através de tipo MIME autêntico (não apenas extensão de arquivo que pode ser falsificada) garantindo que apenas tipos permitidos sejam aceitos e bloqueando uploads de formatos potencialmente perigosos (executáveis scripts macros) que possam representar riscos de segurança. O tamanho máximo de 10MB por arquivo é validado tanto no frontend quanto backend, onde frontend apresenta feedback imediato quando arquivo excede limite sugerindo compressão ou divisão, enquanto backend garante enforcement da regra mesmo se validação client-side for bypassed. Sistema armazena metadados completos de cada documento incluindo nome original do arquivo, tamanho em bytes, tipo MIME, hash SHA-256 para verificação de integridade, timestamp de upload, usuário responsável e entidade à qual documento está vinculado. Implementado nos módulos GEOWEB, REURBCAD e GEOAPI com prioridade Must-have, este recurso é fundamental para gestão documental integrada ao cadastro territorial permitindo anexação de comprovantes, certidões e outros documentos essenciais aos processos de regularização fundiária.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
