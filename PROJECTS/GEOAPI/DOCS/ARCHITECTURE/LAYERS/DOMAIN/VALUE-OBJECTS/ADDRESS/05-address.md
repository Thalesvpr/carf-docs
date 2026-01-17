# Address

Value object imutável herdando de BaseValueObject representando endereço completo brasileiro com todos os componentes necessários para localização física e geração de documentos oficiais de regularização fundiária. Campos obrigatórios incluem Logradouro (tipo + nome da rua como "Rua das Flores", "Avenida Brasil"), Numero (string permitindo "S/N" para sem número), Bairro e Cidade com validações de não-vazio.

Campos opcionais incluem Complemento (apartamento, bloco, sala), CEP (string formatada "00000-000" com validação de 8 dígitos), Estado (sigla UF de 2 letras maiúsculas), e Referência (ponto de referência textual para facilitar localização em áreas informais onde numeração oficial é inexistente).

Métodos principais incluem construtor validando campos obrigatórios, ToString() retornando endereço formatado completo "Logradouro, Numero - Complemento - Bairro, Cidade/UF, CEP", ToShortString() retornando versão resumida "Logradouro, Numero - Bairro", e operadores de igualdade comparando todos os campos normalizados. Usado em Unit para endereço oficial da propriedade em certidões e memoriais descritivos, permitindo coexistência com geometria GeoPolygon (endereço textual + perímetro espacial) e suportando tanto áreas urbanas formais com CEP quanto assentamentos informais onde referência textual é mais relevante.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
