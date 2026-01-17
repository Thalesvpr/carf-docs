---
modules: [GEOWEB, GEOGIS]
epic: scalability
---

# UC-008-FE-001: Arquivo Inválido

Fluxo de exceção do UC-008 Importar Shapefile ocorrendo no passo 5.2 durante validação de arquivo quando sistema detecta que arquivo uploadado não é Shapefile válido verificando uma ou mais condições de invalidade incluindo ZIP não contém arquivo .shp (componente principal com geometrias binário obrigatório), ZIP não contém arquivo .dbf (tabela de atributos dBase obrigatória), arquivos .shp e .dbf possuem nomes base diferentes (ex: unidades.shp mas titulares.dbf indicando arquivos de Shapefiles diferentes compactados juntos incorretamente), magic number do .shp diferente de 9994 indicando arquivo corrompido ou formato diferente renomeado incorretamente, version number do .shp diferente de 1000 indicando versão Shapefile não suportada, ou estrutura DBF corrompida com header inválido impedindo leitura de campos, tipicamente causado por usuário compactar arquivos incorretos selecionando apenas .shp esquecendo .dbf .shx necessários, ou renomear arquivo .dwg CAD para .shp sem converter formato realmente, ou corrupção durante transferência FTP com modo texto ao invés de binário alterando bytes, sistema ao detectar invalidade interrompe processamento antes de criar job evitando tentar importar dados corrompidos que causariam falhas em cascata no worker, exibe modal vermelho erro com ícone de alerta título "Arquivo Inválido" mensagem específica detalhando problema encontrado oferecendo orientações corretivas como "Arquivo inválido. Certifique-se de incluir os arquivos obrigatórios: .shp (geometrias), .dbf (atributos), .shx (índice). Opcionais: .prj (projeção), .cpg (codificação)" listando componentes necessários, inclui link clicável "Como preparar Shapefile para importação?" abrindo documentação com tutorial passo-a-passo mostrando screenshots de QGIS exportando corretamente Shapefile com todos componentes, exibe botão Tentar Novo Upload limpando dropzone e permitindo usuário selecionar arquivo correto após corrigir problema, loga erro em sistema de logging incluindo filename uploaded_by timestamp e error_details facilitando troubleshooting se usuário reportar problema recorrente indicando bug em validação ou necessidade de melhorar mensagens de erro tornando mais claras, opcionalmente pode oferecer validação preventiva client-side usando JavaScript FileReader lendo arquivos antes de upload verificando presença de .shp e .dbf no ZIP exibindo warning amarelo "Atenção: .prj não encontrado. Sistema assumirá EPSG:4326" orientando antes mesmo de enviar ao servidor economizando round-trip e melhorando feedback imediato.

**Ponto de Desvio:** Passo 5.2 do UC-008 (validação após upload)

**Retorno:** Upload bloqueado, usuário corrige arquivo e tenta novamente

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
