# DescriptiveMemorial

Entidade representando memorial descritivo documento técnico topográfico descrevendo perímetro Unit coordenadas geodésicas vértices confrontações azimutes distâncias elaborado Surveyor seguindo normas NBR 13133 Lei 10267 permitindo identificação inequívoca imóvel regularização registro. Herda de BaseEntity fornecendo auditoria temporal. Campos principais incluem UnitId Guid FK unidade descrita, CertificateId Guid nullable FK LegitimationCertificate se gerado junto, SurveyorId Guid FK responsável técnico, MemorialNumber string único (MEM-2025-00045) e ArtNumber string nullable CREA responsabilidade.

Campos técnicos incluem Content string texto formatado padrão (Inicia-se descrição perímetro vértice P1 coordenadas E=... N=... azimute... distância... até P2...), Vertices JSON array vértices UTM geográficas processamento programático, Confrontations JSON mapeando lados confrontantes (P1-P2 Rua Flores, P2-P3 João Silva), Area decimal m² Gauss, Perimeter decimal metros, Datum string SIRGAS2000 e Zone string UTM (23S 24S). Campos armazenamento PdfPath S3 PDF, GeneratedAt DateTime, GeneratedBy Guid FK Account e Observations string nullable.

Métodos incluem GeneratePdf() template NBR 13133 IPdfGenerator cabeçalho ART coordenadas assinatura, CalculateArea() Gauss comparando Unit.Area tolerância 5%, CalculatePerimeter() distâncias vértices, ValidateVertices() fechamento polígono tolerância 0.01m e AddVertex()/UpdateConfrontation(). Regra negócio Unit mínimo 3 SurveyPoint Status APPROVED, Vertices mínimo 3, SurveyorId CREA válido, ArtNumber obrigatório oficiais e Datum SIRGAS2000. Participa LegitimationPlan coordenadas plotadas graficamente.

---

**Última atualização:** 2026-01-12
