# WORKFLOWS

Workflows descrevem sequências de atividades coordenadas entre atores humanos e sistema, atravessando múltiplos aggregates para completar processos de negócio end-to-end.

A documentação segue princípio technology-agnostic, usando termos genéricos como "banco de dados relacional" e "ferramenta GIS desktop" sem mencionar tecnologias específicas. Detalhes de implementação pertencem a PROJECTS/*/DOCS/.

A ordem dos workflows reflete a sequência temporal do processo real, desde configuração inicial até certificação final.

## Workflows Documentados

1. **[01-wms-integration-workflow.md](./01-wms-integration-workflow.md)** - Configuração e consumo de ortofotos via WMS/WMTS OGC para visualização de imagens aéreas como base cartográfica.

2. **[02-field-data-collection-workflow.md](./02-field-data-collection-workflow.md)** - Coleta de dados em campo usando app mobile offline-first, capturando geometrias, fotos e informações de titulares.

3. **[03-offline-sync-workflow.md](./03-offline-sync-workflow.md)** - Sincronização bidirecional entre mobile e backend com detecção e resolução de conflitos.

4. **[04-analyst-validation-workflow.md](./04-analyst-validation-workflow.md)** - Validação e correção em massa de geometrias usando ferramenta GIS desktop com ortofotos sobrepostas.

5. **[05-topography-workflow.md](./05-topography-workflow.md)** - Levantamento topográfico profissional com GNSS e pós-processamento via estações RBMC para precisão centimétrica.

6. **[06-legitimation-workflow.md](./06-legitimation-workflow.md)** - Processo completo de legitimação fundiária conforme Lei 13.465/2017, desde submissão até emissão de certidão.

---

**Última atualização:** 2026-01-14
