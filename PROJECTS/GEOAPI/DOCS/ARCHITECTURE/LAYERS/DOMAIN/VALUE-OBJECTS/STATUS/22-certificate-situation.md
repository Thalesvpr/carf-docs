# CertificateSituation

Value object enum representando situação do imóvel na certidão de legitimação fundiária conforme terminologia técnica registral e requisitos da Lei 13.465/2017. Valores possíveis são COVERED (imóvel encravado totalmente dentro de outro imóvel maior, confrontando com área remanescente em todas as divisas), CONFRONTING (imóvel confinante fazendo divisa com outro imóvel ou via pública mas não encravado, possui frente para logradouro), e BOTH (situação mista onde imóvel está parcialmente encravado e parcialmente confrontante).

Métodos incluem RequiresRemainingArea() retornando true para COVERED e BOTH que devem especificar RemainingArea, RequiresConfrontations() retornando true para todos com detalhamento diferente, GetLegalDescription() retornando template de texto legal seguindo padrões de memorial descritivo cartorial, IsValidForRegistration() verificando se permite registro direto (CONFRONTING) ou requer matrícula mãe (COVERED/BOTH), e ToDisplayString() retornando descrição amigável.

Usado em LegitimationCertificate.Situation determinando como DescriptiveMemorial e LegitimationPlan devem descrever o imóvel, valida que COVERED tem TotalArea e RemainingArea corretas, influencia templates de geração de PDF usando linguagem registral apropriada, e orienta cartório de registro de imóveis sobre procedimentos de matriculação.

---

**Última atualização:** 2026-01-12
