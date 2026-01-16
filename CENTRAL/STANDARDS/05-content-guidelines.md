# Diretrizes de Conteúdo

Documentos devem seguir diretrizes de tamanho e densidade que garantem qualidade e legibilidade do conteúdo.

## Limites de Tamanho por Tipo

Cada tipo de documento possui limites mínimos e máximos de palavras. READMEs devem ter entre 50 e 500 palavras. ADRs devem ter entre 200 e 800 palavras. Casos de uso devem ter entre 150 e 800 palavras. Requisitos funcionais devem ter entre 80 e 400 palavras. Requisitos não funcionais devem ter entre 60 e 350 palavras. User stories devem ter entre 60 e 300 palavras. Entidades devem ter entre 150 e 600 palavras. Features devem ter entre 200 e 1000 palavras. How-tos devem ter entre 150 e 900 palavras. Conceitos devem ter entre 100 e 600 palavras. Regras de negócio devem ter entre 100 e 800 palavras. Workflows devem ter entre 150 e 1000 palavras. Patterns devem ter entre 200 e 900 palavras.

## Densidade de Conteúdo

Documentos devem manter densidade adequada evitando parágrafos fragmentados. Requisitos funcionais devem ter mínimo de 800 caracteres de conteúdo com no máximo 2 parágrafos por seção e entre 20 e 50 palavras por sentença. User stories devem ter mínimo de 1000 caracteres com no máximo 2 parágrafos e entre 25 e 60 palavras por sentença. Entidades devem ter mínimo de 1500 caracteres com no máximo 2 parágrafos e entre 35 e 100 palavras por sentença. Regras de negócio devem ter mínimo de 800 caracteres com no máximo 3 parágrafos e entre 15 e 45 palavras por sentença. Casos de uso devem ter mínimo de 600 caracteres com no máximo 3 parágrafos e entre 20 e 50 palavras por sentença.

## Uso de Listas

Listas com bullet points são permitidas apenas em seções estruturadas específicas. Seções que permitem bullets incluem: Fluxos Alternativos, Fluxos de Exceção, Regras de Negócio, Rastreabilidade, Critérios de Aceitação, Relacionamentos, Módulos, Pré-condições, Pós-condições, Atores, Referências, Ver também, Dependências, Estrutura, Aplicações, Bibliotecas e Domínios. No corpo principal do documento deve-se usar prosa contínua ao invés de listas.

## Continuidade de Prosa

O conteúdo deve fluir naturalmente sem quebras excessivas. Evitar parágrafos órfãos com menos de 50 palavras isolados entre seções. Evitar mais de 3 quebras de linha consecutivas. Manter densidade adequada de pontuação com vírgulas e conectores para criar texto coeso.

## Validação

Os scripts em .scripts/carf_validator validam tamanho com códigos SIZE001 e SIZE002, densidade com códigos DENS001 a DENS004, bullets com código BULLET001, e continuidade com códigos PROSE001 a PROSE003.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
