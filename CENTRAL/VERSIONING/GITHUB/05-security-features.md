---
type: leaf
status: rejected
description: "Conteudo operacional. Git workflows pertencem a .github ou CONTRIBUTING."
updated: 2026-01-20
---

# Features de Segurança

Recursos de segurança do GitHub habilitados nos repositórios CARF para detecção proativa de vulnerabilidades, gestão de dependências e proteção contra vazamento de secrets.

## Dependabot

Dependabot monitora dependências e cria pull requests automáticos quando novas versões ou patches de segurança estão disponíveis. Configuração fica em .github/dependabot.yml especificando package ecosystems (npm, nuget, pip, docker), diretórios a monitorar, frequência de verificação (daily ou weekly) e limites de PRs abertos simultaneamente.

## Dependabot Alerts

Alerts notificam sobre vulnerabilidades conhecidas (CVEs) em dependências do projeto. Severidade é classificada como Critical, High, Medium ou Low. Vulnerabilidades Critical e High devem ser corrigidas em até 7 dias. Medium em até 30 dias. Low podem ser priorizadas conforme roadmap.

## CodeQL Analysis

CodeQL executa análise estática de segurança (SAST) identificando padrões de código vulneráveis como SQL injection, XSS, path traversal e authentication bypass. Workflow .github/workflows/codeql.yml executa em push e pull request. Findings são exibidos na aba Security do repositório.

## Secret Scanning

GitHub detecta automaticamente secrets commitados acidentalmente como API keys, tokens e passwords. Push protection bloqueia commits contendo patterns conhecidos de secrets. Alerts são criados para secrets detectados em histórico. Secrets vazados devem ser revogados imediatamente e rotacionados.

## Configuração por Repositório

| Feature | carf-geoapi | carf-geoweb | carf-keycloak |
|---------|-------------|-------------|---------------|
| Dependabot Updates | nuget, docker | npm | maven, docker |
| Dependabot Alerts | Habilitado | Habilitado | Habilitado |
| CodeQL Languages | csharp | javascript, typescript | java |
| Secret Scanning | Habilitado | Habilitado | Habilitado |
| Push Protection | Habilitado | Habilitado | Habilitado |

## Security Policy

Cada repositório deve ter arquivo SECURITY.md descrevendo como reportar vulnerabilidades de forma responsável. O arquivo especifica contato para reports, tempo esperado de resposta e processo de disclosure. Vulnerabilidades reportadas são tratadas com confidencialidade até correção ser publicada.

## Revisão de Segurança

Maintainers devem revisar Security tab semanalmente verificando alerts pendentes, PRs do Dependabot aguardando merge e findings do CodeQL. Métricas de tempo médio de resolução (MTTR) para vulnerabilidades são acompanhadas mensalmente.

## Práticas Recomendadas

Nunca commitar secrets em código, usar variáveis de ambiente e secrets do GitHub Actions. Manter dependências atualizadas mergeando PRs do Dependabot regularmente. Revisar findings do CodeQL mesmo quando classificados como false positives para confirmar. Habilitar branch protection para impedir bypass de security checks.
