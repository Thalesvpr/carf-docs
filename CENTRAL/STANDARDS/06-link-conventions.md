# Convenções de Links

Links internos entre documentos seguem convenções específicas que garantem navegabilidade e evitam referências quebradas.

## Formato de Paths

Todos os links internos devem usar paths relativos começando com ponto e barra como ./pasta/arquivo.md. Paths absolutos Windows como C:\DEV\ não são permitidos. Paths absolutos Unix como /home/user/ não são permitidos.

## Diretórios em CENTRAL

Diretórios dentro de CENTRAL devem usar nomes em UPPERCASE. Links para estes diretórios devem respeitar o case como ./DOMAIN-MODEL/README.md. Links para diretórios devem sempre apontar para o README interno como ./PASTA/README.md ao invés de apenas ./PASTA/.

## Isolamento CENTRAL e PROJECTS

CENTRAL é a fonte de verdade e não deve depender de PROJECTS. Documentos em CENTRAL não podem conter links para documentos em PROJECTS. Documentos em PROJECTS devem referenciar CENTRAL quando apropriado, linkando para requisitos, casos de uso e definições centrais ao invés de duplicar conteúdo.

## Referências Cruzadas

Documentos em PROJECTS que implementam requisitos de CENTRAL devem conter links de rastreabilidade. Features devem referenciar os RFs que implementam. Entidades devem referenciar definições do modelo de domínio central. A ausência de referências a CENTRAL em documentos de PROJECTS gera aviso informativo.

## Links Quebrados

Links que apontam para arquivos inexistentes são erros críticos que devem ser corrigidos. O validador detecta links quebrados verificando se o arquivo alvo existe no filesystem.

## Validação

Os scripts em .scripts/carf_validator validam formato de links com códigos LINK001 a LINK005, links quebrados com código BLINK001, isolamento com códigos ISOL001 e ISOL002, e referências cruzadas com código XREF001.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
