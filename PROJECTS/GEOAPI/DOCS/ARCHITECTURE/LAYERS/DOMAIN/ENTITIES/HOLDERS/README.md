# HOLDERS

Entities gerenciamento titulares do GEOAPI representando pessoas físicas reivindicando posse ou propriedade unidades habitacionais. Holder armazena dados pessoais CPF value object validado algoritmo mod 11, Name completo, BirthDate verificando maior idade legal para ownership brasileiro, Email e PhoneNumber value objects validados, Address residencial e IsActive status, mantendo histórico soft delete compliance LGPD permitindo anonimização sem perder integridade referencial auditoria. UnitHolder junction entity implementando relacionamento N:N entre Unit e Holder adicionando campos semânticos HolderType enum (OWNER/SPOUSE/RESIDENT/OTHER) especificando natureza vínculo familiar, SharePercentage decimal nullable para condomínio pro indiviso quando múltiplos coproprietários, IsPrimary boolean identificando titular principal para comunicações oficiais, DocumentPath string apontando S3 onde certidões casamento documentos comprobatórios armazenados e Notes texto livre justificando vínculos atípicos. Relacionamento permite Unit ter múltiplos Holders e Holder possuir múltiplas Units modelando realidade campo onde famílias extensas ocupam várias moradias e imóveis têm copropriedade complexa requerendo flexibility beyond simple 1:N.

## Arquivos

- **[03-holder.md](./03-holder.md)** - Titular pessoa física reivindicando posse
- **[20-unit-holder.md](./20-unit-holder.md)** - Relacionamento N:N Unit Holder com tipo vínculo

---

**Última atualização:** 2026-01-12
