# Crea

Value object imutável herdando de BaseValueObject representando registro CREA (Conselho Regional de Engenharia e Agronomia) de profissional responsável técnico por levantamentos topográficos, memoriais descritivos e plantas de legitimação. Validações incluem verificação de formato "CREA/UF NNNNN-T" onde UF é sigla do estado (ex: RJ, SP, MG), NNNNN é número de registro de 5 dígitos, e T é dígito verificador calculado.

Métodos principais incluem construtor recebendo string com ou sem formatação (aceita "CREA/RJ 12345-6" ou "CREARJ123456"), ToString() retornando formato legível "CREA/RJ 12345-6", ToUnformatted() retornando versão sem espaços para persistência, UF() extraindo sigla do estado, RegistrationNumber() extraindo apenas dígitos do registro, e operadores de igualdade comparando valores normalizados.

Usado em Surveyor.Crea para identificar profissional habilitado responsável por levantamentos topográficos, validado em SurveyProcessing.SurveyorId garantindo que apenas topógrafos com CREA ativo podem processar dados GPS, e obrigatório em DescriptiveMemorial e LegitimationPlan para cumprir exigência legal de ART em documentos técnicos de regularização fundiária.

---

**Última atualização:** 2026-01-12
