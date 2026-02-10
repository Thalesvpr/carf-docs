---
type: leaf
status: review
updated: 2026-02-07
---

# Scripts de Validacao

Descricao dos scripts TypeScript para validacao da documentacao. Arquivos relacionados: 17-validation-rules.md e 17-validation-ci.md.

## Script Principal (validate-sources.ts)

Script em scripts/validate-sources.ts que importa glob, readFile, access e gray-matter. Define interface Violation com campos ruleId, severity (ERROR, WARNING, INFO), file, line, message e suggestion. Define interface ValidationResult com lista de violations e stats contendo filesChecked, errors, warnings e infos.

A funcao validateSources busca arquivos src/content/docs/**/*.mdx ignorando index.mdx e _*.mdx. Para cada arquivo le frontmatter e aplica regras SRC001 (source obrigatorio), SRC004 (formato do source), SRC002 (arquivo fonte existe verificando no caminho DOCS_REPO_PATH), CONT001 (description entre 50-160 caracteres) e CONT002 (title presente e nao vazio). Variavel DOCS_REPO_PATH default para ../carf-docs.

## Validacao de Links

Funcao validateLinks busca todos arquivos mdx, constroi set de paginas existentes mapeando paths para URLs. Para cada arquivo extrai links com regex e verifica se links internos (que nao sao http, hash ou mailto) apontam para paginas existentes. Links quebrados geram violacao CONT003 com severity ERROR.

## Validacao de Imagens

Funcao validateImages busca todos arquivos mdx e extrai imagens com regex. Verifica se texto alternativo existe (CONT005 WARNING) e se imagens com path /images/ existem em public/images/ (CONT004 ERROR).

## Funcao Main

Funcao principal executa validateSources, validateLinks e validateImages em sequencia. Consolida todas as violations e imprime erros e avisos formatados com rule_id, arquivo e mensagem. Exibe resumo com total de arquivos, erros e avisos. Termina com exit code 1 se houver erros, 0 caso contrario.
