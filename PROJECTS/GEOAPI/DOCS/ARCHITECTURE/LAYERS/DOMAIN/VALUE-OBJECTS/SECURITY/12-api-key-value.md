# ApiKeyValue

Value object imutável herdando de BaseValueObject representando chave de API para autenticação de sistemas externos e scripts automatizados, seguindo formato específico com prefixo identificável e hash criptográfico para armazenamento seguro. Validações incluem verificação de formato "geoapi_sk_" seguido de 32 caracteres alfanuméricos aleatórios gerados criptograficamente, rejeitando qualquer chave que não siga padrão ou tenha comprimento incorreto.

Métodos principais incluem Generate() estático gerando nova chave aleatória usando RNGCryptoServiceProvider, construtor recebendo string completa validando formato, Prefix() retornando parte visível "geoapi_sk_" para identificar tipo de chave, ToHash() gerando SHA256 hash do valor completo para persistência segura nunca armazenando plaintext, Matches(string plainKey) comparando hash armazenado com hash de chave fornecida para autenticação, e ToMasked() retornando versão parcialmente oculta "geoapi_sk_abc...xyz" para UI.

Usado em ApiKey.Value armazenando apenas hash criptográfico no banco de dados, em autenticação de requests onde header "X-API-Key: geoapi_sk_..." é validado hasheando valor e comparando com hashes armazenados, e em exibição de chaves ativas em telas administrativas mostrando versão mascarada por segurança, garantindo que mesmo com acesso ao banco valores originais não podem ser recuperados.

---

**Última atualização:** 2026-01-12
