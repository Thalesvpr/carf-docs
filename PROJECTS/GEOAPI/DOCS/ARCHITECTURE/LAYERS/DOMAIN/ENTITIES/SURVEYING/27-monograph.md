# Monograph

Entidade representando monografia SurveyPoint documentando marco geodésico descrição detalhada instruções acesso fotos croqui permitindo relocação futura ponto outros profissionais seguindo padrão técnico documentação topográfica. Herda de BaseEntity fornecendo auditoria temporal. Campos principais incluem SurveyPointId Guid FK ponto documentado relacionamento 1:1, Description string detalhada local (Marco concreto cravado calçada frente portão escola distante 2.5m meio-fio), AccessInstructions string nullable como chegar e PhotoPaths JSON array caminhos S3 fotos marco 4 cardeais Norte Sul Leste Oeste.

Campos adicionais incluem SketchPath string nullable S3 croqui localização mostrando marco relação referências fixas postes árvores esquinas, Remarks string nullable observações visibilidade obstruções, GeneratedAt DateTime quando gerada, GeneratedBy Guid FK Account técnico campo e PdfPath string nullable S3 PDF completo formatado impressão.

Métodos incluem AddPhoto(s3Path cardinal) adicionando foto array validando path, GeneratePdf() compilando Description AccessInstructions fotos croqui template padrão IPdfGenerator salvando S3, Validate() verificando campos obrigatórios Description não vazio PhotoPaths mínimo 1 foto e GetCardinalPhotos() retornando dicionário direções paths. Regra negócio recomenda 4 fotos cardeais permite mínimo 1, Description mínimo 50 caracteres adequado e Monograph após SurveyPoint Status PROCESSED/APPROVED garantindo coordenadas validadas.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
