---
type: leaf
status: review
updated: 2026-02-08
---

# LegitimationPlan

Entidade representando a planta de legitimacao fundiaria, desenho tecnico cartografico que plota graficamente a Unit com vertices, medidas, confrontacoes, norte geografico, escala e convencoes ABNT. Elaborada por Surveyor como documento visual complementar ao DescriptiveMemorial, permite visualizacao espacial para registro e processos cartoriais. Herda de BaseEntity fornecendo auditoria temporal.

## Propriedades Principais

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| UnitId | Guid | nao | FK para a unidade representada. |
| MemorialId | Guid | nao | FK para o memorial descritivo correspondente, fonte das coordenadas dos vertices. |
| CertificateId | Guid? | sim | FK para LegitimationCertificate quando gerada junto a certidao. |
| SurveyorId | Guid | nao | FK para o responsavel tecnico com CREA valido. |
| PlanNumber | string | nao | Numero unico no formato PLANT-AAAA-NNNNN. |

## Propriedades de Formato

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Format | string | Formato do papel: A4, A3, A2, A1, A0. |
| Scale | string | Escala cartografica: 1:200, 1:500, 1:1000, 1:2000. Relacao entre papel e terreno. |
| Layout | JSON? | Posicionamento de elementos visuais: legenda, indicador de norte, barra de escala, carimbo. |

## Propriedades de Armazenamento

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| DwgPath | string? | Caminho S3 do arquivo DWG/DXF editavel com layers organizados. |
| PdfPath | string | Caminho S3 do PDF para impressao. |
| PngPath | string? | Caminho S3 do preview PNG em 300 dpi para visualizacao rapida. |
| GeneratedAt | DateTime | Timestamp da geracao. |
| GeneratedBy | Guid | FK para Account que gerou. |

## Metodos

| Metodo | Descricao |
|--------|-----------|
| GenerateDwg() | Gera arquivo DXF via netDXF plotando poligono, textos de medidas, azimutes, confrontacoes, indicador de norte, escala e carimbo em layers organizados. |
| GeneratePdf() | Converte DXF para PDF ou gera direto para impressao. |
| GeneratePng() | Gera preview PNG em 300 dpi para exibicao em interface. |
| CalculateScale() | Determina escala adequada considerando area da Unit e formato do papel. |

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| Memorial validado | MemorialId deve referenciar memorial com vertices validos antes de gerar planta. |
| Escala adequada | Escala segue convencoes cartograficas: ate 100m2 usa 1:200, ate 500m2 usa 1:500, acima de 500m2 usa 1:1000 ou maior. |
| Formato compativel | O formato de papel deve comportar a escala escolhida. |
| CREA valido | SurveyorId deve referenciar profissional com CREA ativo. |
| Trio documental | Completa o pacote certidao + memorial + planta para exportacao e entrega a cartorio. |
