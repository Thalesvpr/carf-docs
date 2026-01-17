# Convenções de Nomenclatura

Arquivos de documentação seguem convenções de nomenclatura específicas por tipo, garantindo identificação rápida e organização consistente em todo o repositório.

## Prefixos por Tipo

Casos de uso usam prefixo UC seguido de número sequencial com três dígitos e nome descritivo em kebab-case, resultando em formato UC-001-nome-do-caso.md. Requisitos funcionais usam prefixo RF com mesmo padrão numérico, resultando em RF-001-nome-do-requisito.md. User stories usam prefixo US resultando em US-001-nome-da-story.md. Requisitos não funcionais usam prefixo RNF resultando em RNF-001-nome-do-requisito.md. Architecture Decision Records usam prefixo ADR resultando em ADR-001-titulo-da-decisao.md.

## Títulos por Tipo

O título H1 de cada documento deve seguir padrão específico por tipo. Requisitos funcionais, casos de uso, user stories, requisitos não funcionais e ADRs devem ter título no formato PREFIXO-NNN: Título Descritivo, como RF-001: Integração com Keycloak ou UC-001: Cadastrar Unidade Habitacional. READMEs devem ter título em maiúsculas ou no formato Nome - Descrição.

## Numeração Obrigatória

Todo arquivo markdown exceto README.md deve ter prefixo numérico obrigatório. Arquivos de requisitos usam seus prefixos específicos como RF-001, US-002, UC-003, RNF-004, ADR-005. Demais arquivos usam prefixo numérico de dois dígitos seguido de hífen como 01-nome.md, 02-nome.md. A numeração começa em 01 e segue ordem lógica de leitura ou dependência. Arquivos sem numeração são erros de validação com código NUM001. Arquivos em pastas SRC-CODE e .scripts são isentos desta regra.

## Pastas de Domínio

Pastas que agrupam requisitos por domínio usam prefixo numérico de dois dígitos seguido de nome do domínio em kebab-case. Exemplos incluem 01-auth-security, 02-tenants, 03-users-teams. A numeração indica ordem de prioridade ou dependência entre domínios.

## Kebab-Case

Todos os nomes de arquivo e pasta usam kebab-case com letras minúsculas e palavras separadas por hífen. Acentos e caracteres especiais são permitidos em português quando necessário para clareza, como RF-001-validação-cpf.md. Espaços nunca são usados em nomes de arquivo.

## Terminologia Técnica

Termos técnicos devem seguir grafia oficial do produto ou tecnologia. Usar PostgreSQL ao invés de Postgres ou postgres. Usar PostGIS ao invés de Postgis. Usar Keycloak ao invés de KeyCloak ou keycloak. Usar React Native ao invés de react-native em prosa. Usar .NET ao invés de DotNet ou dotnet. Usar Node.js ao invés de Nodejs ou NodeJS. Usar TypeScript ao invés de Typescript. Usar JavaScript ao invés de Javascript. Usar REURB-S ou REURB-E ao invés de REURB sem qualificador.

## READMEs

Todo diretório deve conter arquivo README.md com R maiúsculo. Este é o único arquivo que não segue convenção de prefixo pois serve como índice e ponto de entrada da pasta. Diretórios em CENTRAL devem usar nomes em UPPERCASE.

## Validação

Os scripts em .scripts/carf_validator validam títulos com códigos TITLE001 a TITLE003, terminologia com código NOMEN001 e numeração obrigatória com código NUM001.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review
