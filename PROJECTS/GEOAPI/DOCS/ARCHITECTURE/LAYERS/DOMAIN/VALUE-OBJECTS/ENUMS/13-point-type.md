# PointType

Value object enum representando tipo de ponto topográfico coletado em campo durante levantamentos geodésicos, determinando precisão esperada, método de coleta e uso em processamentos posteriores. Valores possíveis são MARCO (marco geodésico permanente materializado com concreto, chapa metálica ou estaca com coordenadas processadas de alta precisão servindo como referência fixa), PIQUETE (piquete temporário cravado no solo marcando vértice de perímetro removível após conclusão), e NATURAL (ponto natural estável como afloramento rochoso ou quina de construção usado como referência quando marcos artificiais não são viáveis).

Métodos incluem IsPermanent() retornando true para MARCO, RequiresMonograph() verificando se tipo exige monografia descritiva (apenas MARCO), MinimumPrecision() retornando precisão mínima esperada em centímetros (MARCO ≤2cm, PIQUETE ≤5cm, NATURAL ≤10cm), e ToDisplayString() retornando descrição amigável.

Usado em SurveyPoint.Type para classificar pontos coletados, validado em Monograph garantindo que apenas MARCO recebe monografia completa com fotos e croqui de acesso, influencia em SurveyProcessing.PrecisionX/Y/Z verificando se precisão atende requisito do tipo, e determina apresentação em LegitimationPlan onde MARCO aparece com simbologia destacada enquanto PIQUETE é apenas referencial.

---

**Última atualização:** 2026-01-12
