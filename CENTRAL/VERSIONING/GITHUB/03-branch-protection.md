# Proteção de Branches

Regras de proteção da branch main em todos os repositórios CARF garantindo qualidade do código através de reviews obrigatórios, checks automatizados e restrições de push direto.

## Regras para Branch Main

A branch main é protegida em todos os repositórios com regras que impedem push direto, exigem pull requests com reviews aprovados e requerem que status checks passem antes do merge. Estas proteções garantem que código em main está sempre em estado deployable.

## Configuração Padrão

| Regra | Valor | Descrição |
|-------|-------|-----------|
| Require pull request before merging | Habilitado | Proíbe push direto para main |
| Required approvals | 2 | Mínimo de dois reviewers para aprovar |
| Dismiss stale reviews | Habilitado | Invalida approvals quando novos commits são adicionados |
| Require review from code owners | Habilitado | CODEOWNERS devem aprovar mudanças em suas áreas |
| Require status checks | Habilitado | CI deve passar antes do merge |
| Require branches to be up to date | Habilitado | Branch deve estar atualizada com main |
| Require conversation resolution | Habilitado | Todos os comentários devem ser resolvidos |
| Require signed commits | Desabilitado | Opcional por enquanto |
| Require linear history | Habilitado | Apenas squash ou rebase merge |
| Do not allow bypassing | Habilitado | Nem admins podem burlar regras |

## Status Checks Requeridos

Cada repositório define seus status checks obrigatórios conforme stack. carf-geoapi requer build, test e lint do .NET. carf-geoweb requer build, test, lint e type-check do TypeScript. carf-reurbcad requer build, test e lint do React Native. carf-geogis requer lint e test do Python. carf-keycloak requer build da imagem Docker e testes.

## Arquivo CODEOWNERS

Cada repositório deve ter arquivo CODEOWNERS na raiz ou em .github/ especificando responsáveis por diferentes áreas do código. Formato usa paths com glob patterns seguidos de usernames ou teams. Exemplo: /src/auth/ @backend-team indica que mudanças em auth requerem aprovação do backend-team.

## Configuração via CLI

Para configurar branch protection usar gh api repos/OWNER/REPO/branches/main/protection com método PUT passando JSON com regras. Para visualizar proteções atuais usar gh api repos/OWNER/REPO/branches/main/protection. Para remover proteção temporariamente (emergências) usar método DELETE no mesmo endpoint.

## Bypass em Emergências

Em situações críticas de produção, maintainers podem solicitar bypass temporário das proteções para hotfix urgente. O bypass deve ser documentado em issue, revertido imediatamente após o hotfix e revisado em postmortem para evitar recorrência.

---

**Status:** Review
**Atualizado:** 2026-01-20
**Descrição:**
