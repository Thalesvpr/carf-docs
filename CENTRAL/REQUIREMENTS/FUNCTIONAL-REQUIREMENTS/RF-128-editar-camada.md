---
modules: [GEOAPI, GEOWEB]
epic: audit
---

# RF-128: Editar Camada

Este requisito especifica que administradores devem poder editar configurações de camadas existentes para ajustar apresentação organização e comportamento sem necessidade de recriar camada e migrar dados, onde interface de edição permite modificar propriedades mantendo features associadas intactas. O sistema deve permitir atualização de nome da camada para renomeação descritiva, modificação de estilo visual incluindo cores espessuras e ícones permitindo refinamento da apresentação conforme necessidades evoluem, e alteração de visibilidade padrão para controlar comportamento inicial ao carregar mapa. A interface deve incluir funcionalidade de reordenação de layers permitindo ajustar Z-index relativo entre camadas, onde mudança na ordem afeta como camadas são empilhadas no mapa com camadas superiores renderizadas sobre inferiores, crítico para garantir que informações mais importantes permaneçam visíveis. Todas as alterações realizadas em configuração de camada devem gerar entradas no log de auditoria registrando usuário responsável timestamp e descrição das mudanças efetuadas, garantindo rastreabilidade completa de evolução da configuração. O sistema deve validar que alterações não quebrem integridade de features existentes, por exemplo impedindo mudança de tipo de geometria se já existem features na camada. A funcionalidade deve estar disponível nos módulos GEOWEB através de interface administrativa e GEOAPI via endpoint PATCH.

---

**Última atualização:** 2025-12-30