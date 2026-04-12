---
type: leaf
status: approved
updated: 2026-02-06
---

# Holder Validation

Regras de validacao aplicadas a entidade Holder garantindo integridade de dados pessoais, unicidade de identificacao e compliance LGPD. CPF ou CNPJ deve ser valido conforme algoritmo de digitos verificadores da Receita Federal, sendo unico por tenant. Exatamente um dos campos deve estar preenchido identificando pessoa fisica ou juridica.

Nome completo requer minimo duas palavras. Email segue RFC 5322 e telefone formato brasileiro com DDD valido. Data de nascimento deve ser passada com idade minima de 18 anos para titular principal. Vinculos com unidades via UnitHolder exigem soma de percentuais nao excedendo 100% e exatamente um titular primario por unidade.

## Unicidade de Titulo

Titular pessoa fisica pode estar vinculado como titular principal a no maximo uma unidade. Se CPF ja consta como titular principal em outra unidade, sistema bloqueia novo vinculo e orienta cadastrador a registrar familiar elegivel. Cotitularidade com conjuge na mesma unidade e permitida. Regra visa garantir distribuicao justa de titulos conforme Lei 13.465/2017.

## Fluxo de Cadastro CPF-Primeiro

CPF e primeiro campo a ser preenchido no cadastro de titular. Demais campos permanecem desabilitados ate validacao do CPF. Validacao verifica: formato correto, digitos verificadores, unicidade no tenant, e ausencia de vinculo como titular principal em outra unidade.

## Obrigatoriedade Condicional - Estado Civil

Se estado civil igual a Casado ou Uniao Estavel, campos do conjuge sao obrigatorios: nome completo e CPF. Campo uniao estavel possui tres opcoes: nao, reconhecida em cartorio, nao reconhecida em cartorio.

## Campos de Formulario

**Filiacao**: campo unico substituindo campos separados de pai e mae. Aceita um ou dois nomes sem exigir identificacao de genero. Acomoda situacoes de registro apenas paterno ou materno. **Campo opcional** - existem pessoas registradas apenas com pai OU apenas com mae, ou que desconhecem filiacao.

**Tempo de Moradia**: campo declaratorio (ex: "5 anos", "mais de 20 anos"). NAO e data especifica mes/ano, pois morador raramente lembra quando se mudou. Aceita valores aproximados.

**Ocupacao**: substitui campo "Vinculo Empregaticio". Valores: empregado formal, autonomo, aposentado, pensionista, desempregado, do lar, estudante, outros.

**Profissao**: lista suspensa com busca baseada em CBO simplificada. Se "outros" selecionado, campo texto descritivo obrigatorio.

**Escolaridade**: dropdown com niveis padronizados. Se "outros", texto obrigatorio.

## Documentacao

Ao menos um documento de identificacao (CPF, RG ou CNH) deve estar anexado antes de aprovacao. Comprovante de residencia requer data recente quando exigido pela modalidade. Para REURB-S, renda declarada nao pode exceder 3 salarios minimos. Sistema detecta duplicatas potenciais comparando CPF, similaridade de nome e proximidade de endereco alertando analista para decisao.

## Regra do Campo Outros

Em qualquer dropdown onde usuario seleciona "Outros", campo texto descritivo torna-se obrigatorio. Formulario nao pode ser salvo com "Outros" selecionado e texto vazio.
