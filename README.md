# CARF - Sistema de Regularização Fundiária Urbana

Sistema para gestão de processos de regularização fundiária urbana conforme Lei 13.465/2017, permitindo que prefeituras gerenciem todo o ciclo desde o cadastramento de unidades habitacionais em campo até a emissão de títulos de legitimação.

A arquitetura é composta por [projetos independentes](./PROJECTS/README.md) que incluem o backend .NET com API REST geoespacial, portal web para analistas, app mobile para coleta em campo offline, plugin QGIS para análises espaciais, console admin para gerenciar usuários, e bibliotecas compartilhadas entre os projetos.

A documentação fica organizada em duas partes principais. A [documentação central](./CENTRAL/README.md) contém a especificação do sistema como um todo, servindo como **fonte única de verdade** para requisitos, arquitetura e regras de negócio. Os [projetos de implementação](./PROJECTS/README.md) contêm a documentação técnica **específica** de cada um, explicando como implementam o que está especificado.

## Documentação

- **[CENTRAL/](./CENTRAL/README.md)** - Documentação centralizada cross-project
- **[PROJECTS/](./PROJECTS/README.md)** - Projetos de implementação

---

**Versão:** v1.0.0 MVP
**Status:** Em planejamento
**Licença:** Proprietário
**Última atualização:** 2026-01-14
