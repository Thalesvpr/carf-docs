---
modules: [GEOWEB, REURBCAD]
epic: holders
---

# RF-090: Campos de Pessoa Jurídica

O sistema deve capturar conjunto específico de campos para titulares do tipo PESSOA_JURIDICA incluindo razão social (nome legal completo da empresa), nome fantasia (nome comercial utilizado publicamente), CNPJ validado algoritmicamente, inscrição estadual quando aplicável, e identificação de representante legal responsável pela organização. A validação de CNPJ utiliza algoritmo específico de verificação de dígitos verificadores do cadastro nacional de pessoas jurídicas garantindo que apenas números válidos sejam aceitos, aplicando regra de cálculo diferente da validação de CPF apropriada à estrutura do documento empresarial. Os campos específicos de pessoa jurídica (razão social CNPJ inscrição estadual representante legal) são exibidos dinamicamente no formulário apenas quando tipo PESSOA_JURIDICA é selecionado, ocultando-os para pessoas físicas e mantendo interface limpa e contextualmente relevante. O campo representante legal é obrigatório garantindo que toda pessoa jurídica cadastrada tenha indivíduo identificado como responsável pela organização, permitindo comunicação e responsabilização quando necessário contatar titular corporativo. Implementado no módulo GEOAPI com prioridade Must-have, estes campos são essenciais para cadastramento adequado de empresas, cooperativas, associações e outras entidades jurídicas que possam ser titulares de unidades habitacionais em contextos de regularização fundiária ou cadastramento territorial empresarial.

---

**Última atualização:** 2025-12-30
