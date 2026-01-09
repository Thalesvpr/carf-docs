# Ownership Criteria (Critérios de Titularidade)

Critérios de titularidade estabelecendo quem pode ser titular beneficiário de processo de regularização fundiária quantos titulares podem ser vinculados a cada unidade habitacional e quais percentuais de propriedade são permitidos garantindo clareza jurídica sobre direitos de propriedade e evitando conflitos futuros entre co-titulares ou herdeiros após emissão de certidão de regularização. Titular primário deve ser pessoa física brasileira nata ou naturalizada ou estrangeiro com visto permanente de residência no Brasil maior de 18 anos ou emancipado civilmente que exerce posse mansa pacífica e ininterrupta sobre unidade habitacional há pelo menos 5 anos demonstrando animus domini (intenção de dono) através de atos de conservação manutenção melhorias e uso habitual do imóvel como residência própria ou de sua família nuclear comprovados mediante declarações de vizinhos fotografias históricas contas de serviços públicos ou qualquer evidência que ateste exercício de posse qualificada. Co-titulares adicionais podem ser vinculados à mesma unidade habitacional limitados a máximo de 4 pessoas incluindo titular primário sendo permitido cônjuge ou companheiro em união estável registrada ou de fato comprovada por no mínimo 2 anos de convivência, filhos maiores de idade que residem no imóvel e contribuem financeiramente para manutenção familiar, pais ou sogros idosos dependentes que coabitam por necessidade de cuidados ou sustento, ou irmãos em regime de copropriedade quando herdam posse de pais falecidos e mantêm uso conjunto da unidade, sendo vedado incluir como co-titular pessoa que possui outra propriedade urbana ou rural registrada em seu nome exceto se renda familiar conjunta de todos co-titulares não excede 5 salários mínimos caracterizando vulnerabilidade social que justifica flexibilização. Percentuais de propriedade devem somar exatamente 100% da unidade habitacional sendo distribuídos entre titular primário e co-titulares conforme acordado entre partes documentado em declaração assinada com reconhecimento de firma ou testemunhas idôneas onde percentuais podem ser iguais (25% cada para 4 titulares) ou desiguais refletindo contribuição financeira relativa de cada um para aquisição ou manutenção do imóvel, mas titular primário deve sempre deter no mínimo 25% da propriedade garantindo que possui interesse jurídico suficiente para representar unidade em processos administrativos e judiciais futuros relacionados à regularização fundiária. Mudança de titularidade após emissão de certidão de regularização pode ocorrer por venda doação herança ou dissolução de união estável sendo registrada em cartório de registro de imóveis mediante apresentação de escritura pública ou formal de partilha homologada judicialmente, mas dentro de período de 10 anos após emissão da certidão mudança de titularidade para pessoa que não residia originalmente no imóvel regularizado requer anuência prévia do poder público municipal verificando que novo titular atende critérios de elegibilidade REURB e que transferência não configura especulação imobiliária vedada por lei que prevê nulidade de certidão se comprovado uso fraudulento do benefício de regularização. Titularidade conjunta com entidades jurídicas como associações de moradores cooperativas habitacionais ou fundações comunitárias é permitida quando beneficiários optam por regime de propriedade coletiva ao invés de individual sendo cada família beneficiária titular de fração ideal do terreno comum proporcional à área de sua unidade habitacional construída mantendo direito de uso exclusivo de sua unidade mas com propriedade formal compartilhada do solo facilitando gestão de áreas comuns infraestrutura e serviços coletivos em núcleos urbanos densos onde lotes individualizados são inviáveis tecnicamente. Comprovação de posse qualificada exigida para todos titulares inclui demonstração de que ocupação é mansa (sem violência ou clandestinidade), pacífica (sem oposição ou contestação de terceiros), contínua (sem interrupções por abandono temporário superior a 1 ano), com animus domini (intenção de ser dono manifestada por atos inequívocos de proprietário como benfeitorias cercamento plantio construção), e de boa-fé (ocupante acredita legitimamente que tem direito sobre imóvel desconhecendo vícios que possam invalidar sua posse) comprovada mediante conjunto robusto de evidências documentais testemunhais e fotográficas coletadas durante processo de cadastramento e vistoria técnica realizados por equipe de campo treinada.

**Critérios titular primário:**
- Pessoa física brasileira ou estrangeiro com visto permanente
- Maior de 18 anos ou emancipado
- Posse mansa, pacífica, contínua há mínimo 5 anos
- Animus domini comprovado (atos de proprietário)
- Sem outra propriedade urbana/rural (salvo vulnerabilidade)

**Co-titulares permitidos (máximo 4 incluindo primário):**
- Cônjuge ou companheiro (união estável ≥2 anos)
- Filhos maiores residentes contribuindo financeiramente
- Pais ou sogros idosos dependentes coabitantes
- Irmãos em copropriedade por herança

**Percentuais de propriedade:**
- Soma deve ser exatamente 100%
- Distribuição conforme acordo entre co-titulares
- Titular primário: mínimo 25% sempre
- Percentuais podem ser iguais ou desiguais

**Mudança de titularidade pós-certidão:**
- Permitida por venda, doação, herança, dissolução união
- Registro em cartório com escritura ou partilha judicial
- Dentro de 10 anos: requer anuência municipal (evitar especulação)
- Após 10 anos: livre transação sem restrições

**Titularidade coletiva:**
- Associação de moradores, cooperativa, fundação
- Fração ideal proporcional à área da unidade
- Uso exclusivo da unidade + propriedade compartilhada do solo
- Gestão conjunta de áreas comuns e infraestrutura

**Relacionamento com Domain Model:**
- Implementa: `DOMAIN-MODEL/ENTITIES/16-unit-holder.md` (junction entity)
- Valida: `DOMAIN-MODEL/ENTITIES/02-holder.md` (titular requirements)
- Regra: `ownership_percentage` soma = 100%, `is_primary_holder` = true para 1 titular

**Implementações por projeto:**
- Backend .NET: `PROJECTS/GEOAPI/LAYERS/DOMAIN/VALUE-OBJECTS/OwnershipPercentage.cs`
- Frontend React: `PROJECTS/GEOWEB/COMPONENTS/holders/OwnershipManager.tsx`
- Mobile React Native: `PROJECTS/REURBCAD/SCREENS/HolderLinkingForm.tsx`

---

**Última atualização:** 2025-01-06
