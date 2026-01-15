# REURB-E Requirements (Requisitos REURB Interesse Específico)

Requisitos de elegibilidade para modalidade REURB-E (Regularização Fundiária Urbana de Interesse Específico) conforme Lei 13.465/2017 destinada a casos que não se enquadram em REURB-S por excederem limites de área ou renda estabelecendo critérios territoriais documentais e procedimentais que devem ser cumpridos para regularização fundiária com custos compartilhados entre beneficiário e poder público garantindo acesso à titularidade formal mesmo para população de renda média que ocupa núcleos urbanos informais consolidados. Critério de área estabelece limite máximo de 500 metros quadrados por unidade habitacional medidos considerando geometria espacial delimitada em planta técnica georreferenciada excluindo áreas comuns compartilhadas onde unidades entre 250m² e 500m² são enquadradas obrigatoriamente em REURB-E independente de renda familiar do beneficiário, e unidades que excedem 500m² não são elegíveis para nenhuma modalidade de REURB devendo buscar regularização através de procedimentos convencionais de usucapião ou compra e venda formal com custos integrais arcados pelo interessado. Critério de renda familiar não estabelece limite superior permitindo beneficiários de qualquer faixa de renda desde que atendam demais requisitos de ocupação tempo e documentação, mas beneficiários com renda familiar acima de 5 salários mínimos devem arcar com percentual maior dos custos do processo através de tabela progressiva de custos cartoários e registrais subsidiados parcialmente pelo poder público ao invés de isenção total concedida em REURB-S, garantindo sustentabilidade financeira do programa de regularização fundiária e evitando subsídio público desnecessário para população que possui capacidade de pagamento. Critério de uso do imóvel estabelece que unidade pode ser destinada à moradia ou uso misto residencial e comercial desde que característica residencial seja predominante com ao menos 50% da área construída destinada à habitação da família do beneficiário comprovado mediante vistoria técnica, permitindo regularização de unidades que combinam residência com pequeno comércio oficina ou prestação de serviços profissionais refletindo realidade de núcleos urbanos consolidados onde atividades econômicas familiares são integradas ao espaço habitacional. Critério de tempo de ocupação estabelece mesmo requisito de REURB-S exigindo mínimo de 5 anos ininterruptos de posse mansa e pacífica comprovados mediante documentação diversa como contas de serviços públicos históricos de pagamento de IPTU fotografias datadas declarações de vizinhos ou qualquer evidência que demonstre antiguidade da ocupação, mas REURB-E exige comprovação documental mais robusta com ao menos 3 fontes de evidência independentes ao invés de declaração simples aceita em REURB-S refletindo maior capacidade de beneficiários REURB-E de obter e organizar documentação formal. Critério de regularidade fundiária estabelece que terreno onde se situa unidade deve estar em situação passível de regularização seja terreno público municipal estadual ou federal com anuência do ente proprietário para transferência de domínio aos ocupantes, ou terreno particular com concordância expressa do proprietário registrada em cartório autorizando regularização e transferência de propriedade, ou terreno em situação de abandono com proprietário não localizado onde poder público pode iniciar procedimento de usucapião administrativa em nome dos ocupantes após esgotadas tentativas de notificação do proprietário original. Requisitos documentais adicionais de REURB-E incluem apresentação de certidão negativa de débitos municipais do imóvel a ser regularizado demonstrando que não há pendências tributárias acumuladas ou compromisso de parcelamento de eventual dívida existente, licença ambiental simplificada emitida por órgão competente quando unidade se localiza em área de preservação permanente ou zona de proteção ambiental atestando que ocupação não causa dano ambiental significativo ou que medidas mitigadoras foram implementadas, e planta técnica georreferenciada elaborada por profissional habilitado (engenheiro ou arquiteto com registro em conselho profissional) ao invés de croqui simplificado aceito em REURB-S garantindo precisão técnica necessária para registro cartorial formal. Custos de REURB-E seguem tabela progressiva estabelecida por decreto municipal onde beneficiários com renda até 5 salários mínimos pagam 30% dos custos totais de escritura registro e emolumentos com subsídio de 70% pelo poder público, beneficiários com renda entre 5 e 10 salários mínimos pagam 60% dos custos com subsídio de 40%, e beneficiários com renda acima de 10 salários mínimos pagam 100% dos custos sem subsídio mas ainda se beneficiam de procedimentos simplificados e priorização no atendimento em relação a processos convencionais de regularização fundiária que podem levar anos para conclusão.

**Critérios de elegibilidade REURB-E:**
- Área máxima: 500m² por unidade habitacional (mínimo 250m²)
- Renda familiar: sem limite superior (custos proporcionais à renda)
- Uso do imóvel: moradia ou uso misto (mínimo 50% residencial)
- Tempo de ocupação: mínimo 5 anos ininterruptos (comprovação documental robusta)
- Regularidade fundiária: terreno público com anuência, particular com concordância, ou abandono

**Requisitos documentais REURB-E:**
- Certidão negativa de débitos municipais ou compromisso de parcelamento
- Licença ambiental simplificada (se em área de proteção)
- Planta técnica georreferenciada por profissional habilitado
- Comprovação de ocupação com múltiplas fontes independentes

**Custos progressivos REURB-E:**
- Renda até 5 SM: 30% custos (70% subsidiado)
- Renda 5-10 SM: 60% custos (40% subsidiado)
- Renda acima 10 SM: 100% custos (sem subsídio)

**Relacionamento com Domain Model:**
- Valida: `DOMAIN-MODEL/ENTITIES/25-legitimation-request.md` (campo modality = REURB_E)
- Valida: `DOMAIN-MODEL/ENTITIES/01-unit.md` (campo area_sqm entre 250-500)
- Valida: `DOMAIN-MODEL/ENTITIES/14-document.md` (documentos adicionais)

**Implementações por projeto:**
- Backend .NET: (caminho de implementação)
- Frontend React: (caminho de implementação)
- Mobile React Native: (caminho de implementação)

---

**Última atualização:** 2025-01-06
**Status do arquivo**: Pronto
