---
type: leaf
status: review
updated: 2026-02-08
---

# PhoneNumber

Value object imutavel representando numero de telefone brasileiro validado. Utilizado na entidade Holder (coluna phone varchar(20), nullable) como meio de contato. Pode ser celular ou fixo com DDD.

## Regras de Validacao

| Regra | Descricao |
|-------|-----------|
| DDD obrigatorio | Codigo de area de 2 digitos (11 a 99). |
| Celular | 9 digitos iniciando com 9 (ex: 9 1234-5678). |
| Fixo | 8 digitos iniciando com 2 a 5 (ex: 3456-7890). |
| Armazenamento | Apenas digitos sem formatacao. 10 ou 11 digitos. |

## Formato

| Operacao | Formato | Exemplo |
|----------|---------|---------|
| Armazenamento | Apenas digitos | 11912345678 |
| Exibicao | (##) #####-#### ou (##) ####-#### | (11) 91234-5678 |
