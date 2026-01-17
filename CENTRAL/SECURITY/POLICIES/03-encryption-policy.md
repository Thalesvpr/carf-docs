# Encryption Policy

Política de criptografia do CARF protegendo dados em trânsito e em repouso contra acesso não autorizado. Dados em trânsito protegidos via TLS 1.3 (Transport Layer Security) obrigatório todos endpoints HTTPS, certificados Let's Encrypt auto-renovados evitando expiração, cipher suites fortes (AES-256-GCM, ChaCha20-Poly1305) desabilitando algoritmos fracos (RC4, 3DES, SHA1), e HSTS (HTTP Strict Transport Security) header forçando navegadores usar sempre HTTPS. Dados em repouso criptografados nível database (PostgreSQL transparent data encryption ou filesystem LUKS) protegendo contra acesso físico discos, backups criptografados AES-256 antes armazenar cloud S3/Azure Blob, e keys gerenciadas via KMS (Key Management Service AWS/Azure) rotacionadas anualmente. Dados sensíveis específicos (CPF, senhas, tokens) protegidos adicionalmente com hashing irreversível bcrypt cost-factor 12 para passwords impossibilitando decriptação mesmo comprometendo database, CPF/CNPJ armazenados hash SHA-256 para deduplicação permitindo busca sem expor número real, e PII (Personally Identifiable Information) mascarado em logs (CPF 123.456.789-00 logado como ***.***.789-**) prevenindo vazamento acidental. Key management segue rotação anual keys criptografia, separação keys por ambiente (dev/staging/prod), e acesso keys restrito via IAM policies apenas serviços necessários.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
