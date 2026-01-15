# CPF (Cadastro de Pessoa Física)

Value object imutável representando CPF brasileiro validado garantindo que apenas números válidos são aceitos no sistema evitando dados incorretos de titulares. Valor conceitual é texto de exatamente 11 dígitos numéricos ou opcionalmente formatado com pontos e hífen (###.###.###-##) para exibição. Regras de validação incluem deve ter exatamente 11 dígitos após remover formatação, não pode ser sequência repetida (00000000000 até 99999999999 são inválidos), deve ter dígitos verificadores corretos calculados por algoritmo oficial da Receita Federal onde décimo dígito é calculado com pesos 10 a 2 sobre primeiros 9 dígitos e décimo primeiro com pesos 11 a 2 sobre primeiros 10 dígitos usando módulo 11, e validação deve ocorrer na criação do value object lançando exception se inválido impedindo criação de CPF malformado. Comportamentos incluem igualdade por valor onde dois CPFs com mesmos 11 dígitos são considerados iguais independente de formatação ou instância de memória, formatação para exibição retornando string ###.###.###-## para interface de usuário, desformatação retornando apenas 11 dígitos numéricos para persistência ou comparação, e ToString retornando versão formatada por padrão. Regras de negócio estabelecem que CPF deve ser único por Holder no sistema não permitindo cadastro duplicado de mesma pessoa, é campo sensível LGPD exigindo criptografia em repouso logs de acesso e consentimento para uso, pode ser mascarado em exibições públicas mostrando apenas primeiros 3 e últimos 2 dígitos (###.***.**#-##) protegendo privacidade, e validação deve ocorrer tanto em frontend para feedback imediato quanto em backend para segurança impedindo bypass.

**Módulos:** GEOAPI, GEOWEB, REURBCAD, GEOGIS

---

**Última atualização:** 2026-01-10
**Status do arquivo**: Pronto
