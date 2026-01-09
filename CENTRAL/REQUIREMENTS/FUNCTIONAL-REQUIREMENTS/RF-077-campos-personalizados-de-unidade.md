---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: compatibility
---

# RF-077: Campos Personalizados de Unidade

O sistema deve permitir que administradores (perfil ADMIN) criem campos customizados por tenant estendendo modelo padrão de unidade habitacional para acomodar necessidades específicas de cada projeto ou município, onde definição de campos inclui especificação de tipo de dado (texto número data select booleano) e configurações de validação. Cada campo customizado pode ter validações específicas como obrigatoriedade, valores mínimos e máximos numéricos, formatos de texto através de expressões regulares, listas de opções predefinidas para campos select, garantindo integridade de dados capturados em campos estendidos com mesmo rigor de campos padrão do sistema. A interface de formulário de unidade exibe dinamicamente campos customizados configurados para o tenant ativo, renderizando controles apropriados (input number select datepicker checkbox) baseados no tipo de cada campo e aplicando validações client-side e server-side conforme regras definidas. Implementado no módulo GEOAPI com prioridade Could-have, este recurso oferece extensibilidade sem modificação de código permitindo adaptação do sistema a contextos diversos de regularização fundiária onde diferentes projetos podem requerer captura de informações específicas não previstas no modelo padrão, mantendo núcleo comum compartilhado e customizações isoladas por tenant.

---

**Última atualização:** 2025-12-30
