---
type: leaf
status: review
updated: 2026-02-08
---

# CertificateSituation

Value object enum representando a situacao do imovel na certidao de legitimacao fundiaria conforme terminologia tecnica registral e requisitos da Lei 13.465/2017. No banco de dados, corresponde ao campo legitimation_certificates.situation (varchar(30)).

A situacao determina como o memorial descritivo e a planta de legitimacao descrevem o imovel, influenciando templates de geracao de PDF e procedimentos de matriculacao em cartorio.

## Valores Permitidos

| Valor | Descricao |
| --- | --- |
| COVERED | Imovel encravado totalmente dentro de outro imovel maior, confrontando com area remanescente em todas as divisas. |
| CONFRONTING | Imovel confinante fazendo divisa com outro imovel ou via publica, possui frente para logradouro. |
| BOTH | Situacao mista onde imovel esta parcialmente encravado e parcialmente confrontante. |

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Area remanescente | COVERED e BOTH devem especificar area remanescente do imovel maior. |
| Confrontacoes | Todos os valores exigem detalhamento de confrontacoes. |
| Registro direto | CONFRONTING permite registro direto; COVERED e BOTH requerem matricula mae. |

Usado em LegitimationCertificate.Situation determinando como DescriptiveMemorial e LegitimationPlan descrevem o imovel, influenciando templates de geracao de PDF e orientando cartorio sobre procedimentos de matriculacao.
