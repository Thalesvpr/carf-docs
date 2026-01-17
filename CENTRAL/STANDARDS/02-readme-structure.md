# Estrutura de README

Todo diretório em CENTRAL e PROJECTS deve conter um arquivo README.md seguindo estrutura padronizada que facilita navegação e compreensão do conteúdo. Arquivos index.md não são permitidos, sempre usar README.md.

## Componentes Obrigatórios

O título deve ser o nome da pasta em formato de heading H1 na primeira linha, seguido de linha em branco. O título deve começar com letra maiúscula. O parágrafo denso deve descrever o propósito e conteúdo da pasta em prosa contínua, incluindo links inline para os arquivos e subpastas filhas. O rodapé deve conter os metadados de status conforme convenção estabelecida, precedido de separador horizontal. A seção de índice é gerada automaticamente por script.

## Parágrafo Denso

O conteúdo principal do README deve ser escrito em parágrafos densos sem uso de code blocks, tabelas ASCII ou listas extensas com bullet points. Links para filhos devem estar embutidos naturalmente no texto usando formato markdown padrão. Cada filho importante deve ser mencionado com contexto suficiente para o leitor entender seu propósito sem precisar abrir o arquivo. READMEs com subpastas devem mencionar a estrutura no parágrafo denso ou ter seção de estrutura antes do rodapé.

## Seções de Estrutura Permitidas

Quando necessário listar subpastas explicitamente fora do parágrafo denso, usar uma das seguintes seções: Estrutura, Aplicações, Bibliotecas, Domínios, Índice ou Arquivos. Links nestas seções devem usar formato com negrito e brackets, como por exemplo NOME entre asteriscos duplos e brackets linkando para o README da pasta, seguido de descrição curta.

## Índice Gerado Automaticamente

O índice de arquivos filhos é gerado automaticamente por scripts Python em .scripts/carf_tree_sync e inserido entre os comentários GENERATED:START e GENERATED:END. Esta seção substitui qualquer listagem manual de arquivos, eliminando duplicação e garantindo que o índice esteja sempre atualizado. O conteúdo entre esses comentários não deve ser editado manualmente pois será sobrescrito na próxima execução do script.

## Hierarquia Linear

READMEs devem linkar apenas para seus filhos diretos nos parágrafos densos, nunca para netos ou arquivos em outras pastas de CENTRAL. Referências a outras áreas devem ser menções textuais sem link, indicando o caminho como PROJECTS/GEOAPI/DOCS/ sem transformar em hyperlink. Isso mantém a navegação hierárquica e evita links quebrados quando arquivos são movidos.

## Formato Final

O arquivo README.md segue esta ordem: título H1 com linha em branco após, parágrafos densos com links para filhos, opcionalmente seção de estrutura, linha horizontal como separador, metadados de status, e por último a seção gerada automaticamente com índice de arquivos. Não deve existir seção manual de estrutura ou lista de arquivos fora da área gerada.

## Validação

Os scripts em .scripts/carf_validator validam estrutura de README com códigos README001 a README007, verificando presença de título, formato correto e seções obrigatórias.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review
