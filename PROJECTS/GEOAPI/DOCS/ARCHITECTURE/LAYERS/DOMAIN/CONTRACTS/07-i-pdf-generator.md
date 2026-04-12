---
type: leaf
status: review
updated: 2026-02-08
---

# IPdfGenerator

Interface abstraindo geracao de PDFs formatados a partir de templates e dados, permitindo criar certidoes, memoriais descritivos, plantas e relatorios oficiais mantendo dominio independente de biblioteca especifica.

## Metodos

| Metodo | Parametros | Retorno | Descricao |
| --- | --- | --- | --- |
| GenerateAsync | string templateName, object model | Stream | Renderiza template com dados retornando PDF. |
| GenerateCertificateAsync | LegitimationCertificate data | Stream | Gera certidao oficial com cabecalho, texto legal, assinatura e QR code. |
| GenerateMemorialAsync | DescriptiveMemorial data | Stream | Gera memorial descritivo com coordenadas e confrontacoes. |
| GeneratePlanAsync | LegitimationPlan data | Stream | Gera planta tecnica com poligono, medidas e escala. |
| SaveAsync | templateName, model, destPath | string | Gera e salva no IFileStorage retornando path. |

Implementada por QuestPdfGenerator usando QuestPDF fluent API ou RazorPdfGenerator usando views Razor. Suporta templates customizaveis por tenant, geracao assincrona em background job, e cache de templates compilados.
