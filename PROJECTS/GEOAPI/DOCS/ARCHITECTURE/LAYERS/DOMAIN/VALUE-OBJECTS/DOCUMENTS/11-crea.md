---
type: leaf
status: review
updated: 2026-02-08
---

# Crea

Value object imutavel herdando de BaseValueObject que representa o registro CREA (Conselho Regional de Engenharia e Agronomia) de profissional responsavel tecnico por levantamentos topograficos, memoriais descritivos e plantas de legitimacao. E obrigatorio em documentos tecnicos de regularizacao fundiaria para cumprir a exigencia legal de ART.

O construtor aceita formatos variados como CREA/RJ 12345-6 ou CREARJ123456 e normaliza internamente. Se o formato for invalido, uma ValidationException e lancada.

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Formato padrao | Segue padrao CREA/UF NNNNN-T onde UF e sigla do estado. |
| UF valida | Sigla de 2 letras maiusculas de estado brasileiro valido. |
| Numero de registro | 5 digitos numericos identificando o profissional. |
| Digito verificador | Digito T calculado para validacao de integridade do registro. |

## Formato

| Aspecto | Especificacao |
| --- | --- |
| ToString() | CREA/RJ 12345-6. |
| ToUnformatted() | Versao compacta sem espacos para persistencia. |
| UF() | Extrai sigla do estado: RJ. |
| RegistrationNumber() | Extrai apenas digitos do registro: 123456. |

Usado em Surveyor para identificar profissional habilitado, validado em SurveyProcessing garantindo que apenas topografos com CREA valido processam dados GPS, e obrigatorio em DescriptiveMemorial e LegitimationPlan para documentos tecnicos oficiais.
