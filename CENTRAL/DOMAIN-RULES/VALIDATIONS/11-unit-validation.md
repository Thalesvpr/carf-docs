---
type: leaf
status: approved
updated: 2026-02-06
---

# Unit Validation

Regras de validacao aplicadas a entidade Unit garantindo integridade de dados espaciais, completude cadastral e compliance com requisitos de regularizacao fundiaria. Codigo deve ser unico dentro da comunidade, gerado automaticamente se nao fornecido. Comunidade e tenant sao obrigatorios.

## Hierarquia

```
Tenant > Community > Block > Plot > Building > Unit
```

Uma unidade pertence a uma edificacao (building). A edificacao pertence a um lote (plot). O campo `buildingId` e opcional pois em casos simples (casa unifamiliar) pode-se omitir a edificacao intermediaria.

Geometria deve ser poligono valido com minimo 3 vertices, sem auto-intersecao, contido dentro dos limites da comunidade. Area deve ser positiva e menor que limite maximo configuravel. Area calculada deve ser consistente com area declarada dentro de tolerancia de 10%. Deteccao de sobreposicao alerta analista sobre conflitos espaciais.

## Transicoes e Documentacao

Ao menos um titular deve estar vinculado antes de transicionar para status de revisao ou aprovacao. Limites de area variam conforme modalidade REURB sendo 250 metros quadrados para interesse social e 500 para interesse especifico. Validacao offline executa subset de regras com flag indicando validacao completa pendente durante sincronizacao.

## Tipo de Utilizacao da Unidade

Classifica o uso do imovel. Distinto do status de atendimento.

| Tipo | Descricao |
|------|-----------|
| Residencial | Moradia |
| Comercio | Uso comercial |
| Misto | Residencia + comercio |
| Terreno vazio | Sem construcao |
| Nao habitado | Construcao abandonada ou em obras |

## Condicao da Unidade

| Condicao | Descricao |
|----------|-----------|
| Ocupada | Em uso regular |
| Vazia | Sem ocupantes no momento |
| Em construcao | Obras em andamento |
| Abandonada | Sem manutencao, deteriorada |

## Obrigatoriedade de Fotos por Status de Atendimento

**Status Presente**: Foto de documento de identificacao do titular obrigatoria. Foto de fachada recomendada mas nao obrigatoria.

**Status Ausente**: Foto de fachada obrigatoria comprovando que agente esteve no local. Campos do titular desabilitados. Cadastro registra apenas: status, localizacao, foto fachada, observacao.

**Status Nao Quis**: Foto de fachada recomendada. Observacao descritiva obrigatoria.

**Status Assinado**: Cadastro completo com assinatura digital do titular. Foto de documento obrigatoria.

## Tipo de Ocupante (Distinto de Status)

| Tipo | Descricao | Elegivel para titulo? |
|------|-----------|----------------------|
| Possuidor | Quem tem posse do imovel | SIM |
| Locatario | Quem aluga o imovel | NAO (contata proprietario) |

Locatario nao recebe titulo. Cadastro registra para contato futuro com proprietario.

## Foto de Fachada

Foto de fachada deve ser capturada exclusivamente pela camera do dispositivo. Acesso a galeria de imagens bloqueado para este tipo de documento, garantindo que foto foi tirada no momento da visita. Preview obrigatorio antes de confirmar, permitindo ao agente verificar qualidade e enquadramento.

Foto de fachada deve ser armazenada vinculada a unidade, nao como documento avulso. Evita confusao na organizacao dos cadastros.
