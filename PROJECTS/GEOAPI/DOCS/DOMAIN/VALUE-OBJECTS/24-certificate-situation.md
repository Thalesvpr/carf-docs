---
type: leaf
status: review
updated: 2026-02-08
---

# CertificateSituation

Value object enum imutavel representando a situacao do imovel na certidao de legitimacao fundiaria. Persiste na coluna situation varchar(30) da tabela legitimation_certificates. Classifica o tipo de regularizacao conforme posicao do imovel em relacao ao nucleo urbano.

## Valores Permitidos

| Valor | Descricao |
|-------|-----------|
| COVERED | Imovel inteiramente dentro do perimetro do nucleo urbano informal. |
| CONFRONTING | Imovel na divisa do nucleo, parcialmente dentro e parcialmente fora. |
| BOTH | Imovel que se enquadra simultaneamente como coberto e confrontante em diferentes trechos. |

## Uso no Dominio

CertificateSituation define o texto legal da certidao emitida e influencia os requisitos documentais. Imoveis CONFRONTING exigem memorial descritivo com demarcacao precisa da divisa entre area regularizada e area externa.
