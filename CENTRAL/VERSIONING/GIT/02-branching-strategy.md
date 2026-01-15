# Branching Strategy

Trunk-based development do CARF com feature branches curtas. Branch main sempre deployable (CI passing, tests green, code reviewed). Feature branches (feature/RF-123-autenticar-usuario) vivem max 2 dias, PR para main com review obrigatória 2 approvals, squash merge mantendo histórico limpo. Release branches (release/v1.2.0) criadas de main quando pronto deploy prod, apenas bugfixes permitidos, tag v1.2.0 após validação staging, merge back main. Hotfix branches (hotfix/fix-rls-policy) de main para bugs prod críticos, fast-track review 1 approval, deploy imediato, tag patch v1.2.1. Branches protegidas: main requer PR + CI + reviews, ninguém push direto. Deletar branches após merge mantendo repo limpo.

---

**Última atualização:** 2025-12-29
**Status do arquivo**: Pronto
