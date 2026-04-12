---
type: leaf
status: review
updated: 2026-02-08
---

# DescriptiveMemorial

Entidade representando o memorial descritivo, documento tecnico topografico que descreve o perimetro de uma Unit com coordenadas geodesicas, vertices, confrontacoes, azimutes e distancias. Elaborado por um Surveyor conforme normas NBR 13133 e Lei 10.267, permite identificacao inequivoca do imovel para regularizacao e registro cartorial. Herda de BaseEntity fornecendo auditoria temporal e soft delete.

## Propriedades Principais

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| UnitId | Guid | nao | FK para a unidade descrita. |
| CertificateId | Guid? | sim | FK para LegitimationCertificate quando gerado junto a certidao. |
| SurveyorId | Guid | nao | FK para o responsavel tecnico com CREA valido. |
| MemorialNumber | string | nao | Numero unico no formato MEM-AAAA-NNNNN. |
| ArtNumber | string? | sim | Numero da ART do CREA. Obrigatorio para memoriais oficiais. |

## Propriedades Tecnicas

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Content | string | Texto formatado seguindo padrao NBR (Inicia-se descricao do perimetro no vertice P1, coordenadas E/N, azimute, distancia). |
| Vertices | JSON | Array de vertices com coordenadas UTM e geograficas para processamento programatico. |
| Confrontations | JSON | Mapeamento de lados e confrontantes (P1-P2: Rua das Flores, P2-P3: Joao Silva). |
| Area | decimal | Area calculada em metros quadrados via formula de Gauss. |
| Perimeter | decimal | Perimetro total em metros, somando distancias entre vertices consecutivos. |
| Datum | string | Sistema de referencia, fixo em SIRGAS2000. |
| Zone | string | Zona UTM (23S, 24S). |
| PdfPath | string | Caminho S3 do PDF gerado com cabecalho, ART, coordenadas e assinatura. |

## Metodos

| Metodo | Descricao |
|--------|-----------|
| GeneratePdf() | Gera PDF usando template NBR 13133 via IPdfGenerator com cabecalho, ART, tabela de coordenadas e campo de assinatura. |
| CalculateArea() | Calcula area via Gauss e compara com Unit.Area com tolerancia de 5%. |
| ValidateVertices() | Verifica fechamento do poligono com tolerancia de 0.01m. Minimo 3 vertices. |

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| Vertices minimos | Unit deve ter no minimo 3 SurveyPoints com status APPROVED. |
| CREA valido | SurveyorId deve referenciar profissional com CREA ativo. |
| ART obrigatoria | ArtNumber obrigatorio para memoriais de processos oficiais de legitimacao. |
| Datum fixo | Datum deve ser SIRGAS2000 conforme norma brasileira. |
| Integridade geometrica | Poligono de vertices deve fechar com tolerancia de 0.01m. |
