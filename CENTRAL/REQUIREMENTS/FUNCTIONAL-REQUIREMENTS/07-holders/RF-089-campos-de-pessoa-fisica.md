---
modules: [REURBCAD]
epic: usability
---

# RF-089: Campos de Pessoa Física

O sistema deve capturar conjunto abrangente de campos para titulares do tipo PESSOA_FISICA incluindo nome completo, CPF (validado algoritmicamente), RG com órgão emissor e UF, data de nascimento permitindo cálculo de idade, gênero e estado civil (SOLTEIRO CASADO DIVORCIADO VIUVO UNIAO_ESTAVEL), além de informações de contato como telefone fixo, celular e email. A validação de CPF utiliza algoritmo de verificação de dígitos verificadores garantindo que apenas números válidos matematicamente sejam aceitos, apresentando feedback imediato ao usuário durante preenchimento quando CPF informado não passa em verificação de consistência. O campo de email é validado através de expressão regular verificando formato sintático válido (presença de @ domínio válido sem espaços), enquanto telefone é formatado automaticamente durante digitação aplicando máscara adequada conforme quantidade de dígitos (fixo com 10 celular com 11) melhorando experiência do usuário e uniformidade de armazenamento. Implementado no módulo GEOAPI com prioridade Must-have, estes campos são essenciais para identificação inequívoca de pessoas físicas titulares de unidades, possibilitando comunicação efetiva, validação de identidade e geração de documentação oficial durante processo de regularização fundiária que requer dados pessoais completos e validados dos beneficiários.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
