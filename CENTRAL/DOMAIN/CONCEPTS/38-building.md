---
type: leaf
status: approved
updated: 2026-02-06
---

# Edificacao

Estrutura fisica construida sobre um lote que abriga uma ou mais unidades habitacionais. Representa o nivel intermediario entre lote e unidade, essencial para modelar corretamente predios, vilas e conjuntos habitacionais.

Em ocupacoes informais, uma edificacao pode ser desde uma casa simples com uma unica unidade ate um predio de varios andares com dezenas de apartamentos irregulares. A edificacao captura as caracteristicas fisicas da construcao que sao compartilhadas por todas as unidades nela contidas.

## Hierarquia do Modelo

A hierarquia espacial completa e: Comunidade → Quadra → Lote → Edificacao → Unidade. Um lote pode conter multiplas edificacoes (casa principal e edicula, por exemplo). Cada edificacao contem uma ou mais unidades. Em casos simples de casa unifamiliar, existe uma edificacao com uma unica unidade.

## Atributos Principais

Tipo de edificacao classifica a construcao: casa terrea, sobrado, predio, galpao, misto. Numero de pavimentos indica quantos andares a construcao possui. Material predominante registra se e alvenaria, madeira, misto ou outro. Area construida total e a soma das areas de todos os pavimentos.

## Relacao com Unidades

Cada unidade pertence a exatamente uma edificacao. A edificacao fornece contexto espacial comum: endereco base, numero predial, caracteristicas construtivas. Unidades dentro da mesma edificacao compartilham infraestrutura como entrada principal, escadas, corredores.

## Exemplos

| Cenario | Lotes | Edificacoes | Unidades |
|---------|-------|-------------|----------|
| Casa simples | 1 | 1 | 1 |
| Casa + edicula | 1 | 2 | 2 |
| Predio | 1 | 1 | N |
| Vila/conjunto | 1 | N | N |
