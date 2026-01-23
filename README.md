---
status: review
updated: 2026-01-22
type: readme
---

# CARF - Sistema de Regularizacao Fundiaria Urbana

Sistema para gestao de processos de regularizacao fundiaria urbana conforme Lei 13.465/2017, permitindo que prefeituras gerenciem todo o ciclo desde o cadastramento de unidades habitacionais em campo ate a emissao de titulos de legitimacao.

A arquitetura e composta por [projetos independentes](./PROJECTS/README.md) que incluem o backend .NET com API REST geoespacial, portal web para analistas, app mobile para coleta em campo offline, plugin QGIS para analises espaciais, console admin para gerenciar usuarios, e bibliotecas compartilhadas entre os projetos.

A documentacao fica organizada em duas partes principais. A [documentacao central](./CENTRAL/README.md) contem a especificacao do sistema como um todo, servindo como **fonte unica de verdade** para dominio, regras de negocio, requisitos, arquitetura e padroes. Os [projetos de implementacao](./PROJECTS/README.md) contem a documentacao tecnica **especifica** de cada um, explicando como implementam o que esta especificado.

## Estrutura

| Pasta | Proposito |
|-------|-----------|
| [CENTRAL](./CENTRAL/README.md) | Especificacao compartilhada: dominio, regras, requisitos, arquitetura, design system, seguranca |
| [PROJECTS](./PROJECTS/README.md) | Implementacoes: GEOAPI, GEOWEB, REURBCAD, GEOGIS, KEYCLOAK, bibliotecas |

---

**Versao:** v1.0.0 MVP
**Licenca:** Proprietario
