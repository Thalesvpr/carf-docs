# PhoneNumber

Value object imutável herdando de BaseValueObject representando número de telefone brasileiro (fixo ou celular) com validação de formato e DDD, normalizando diferentes entradas para formato padrão armazenável. Validações incluem verificação de 10 dígitos para fixo (DDD + 8 dígitos) ou 11 dígitos para celular (DDD + 9 começando com 9 + 8 dígitos), DDD válido entre 11 e 99 conforme divisão territorial brasileira da Anatel.

Métodos principais incluem construtor recebendo string com ou sem formatação (aceita "(21)98765-4321", "21987654321", "021 9 8765-4321") normalizando para apenas dígitos, ToString() retornando formato legível "(21) 98765-4321" para celular ou "(21) 3456-7890" para fixo, ToUnformatted() retornando apenas dígitos "21987654321" para persistência, IsCellPhone() verificando se é celular, DDD() extraindo código de área, e operadores de igualdade comparando valores normalizados.

Usado em Holder para contato do titular, Surveyor para contato do profissional responsável, e Account para telefone do usuário, permitindo envio de notificações SMS e validação via WhatsApp Business API em workflows de aprovação de documentos.

---

**Última atualização:** 2026-01-12
