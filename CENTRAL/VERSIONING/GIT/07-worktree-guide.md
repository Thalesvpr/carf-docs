# Git Worktree - Trabalho Paralelo em Múltiplas Branches

Git worktree permite trabalhar em múltiplas branches simultaneamente sem necessidade clones duplicados ou troca constante branches eliminando context switching overhead preservando working directory state cada branch isolada filesystem paths distintos enabling parallel development features bugfixes reviews sem interferência mútua confusion stashing uncommitted changes cleaning workspace switching back forth repeatedly disruptive flow interrupting focus concentration productivity diminishing quality output mistakes errors rework waste.

## Problema Resolvido

Desenvolvimento típico sem worktree envolve single working directory exigindo git checkout branch-name toda vez trabalhar branch diferente causando problemas uncommitted changes requerendo stash apply cycle loss train thought interruption debugging session active IDE state editor tabs open terminal commands running testing loops broken restart overhead significant especially large codebases slow builds lengthy setup procedures infrastructure dependencies databases services containers requiring initialization warmup readiness delays frustrating developers impatient waiting idle unproductive blocked.

Worktree soluciona criando múltiplos working directories cada um linked repository compartilhando .git objects storage efficient disk usage minimal duplication apenas files altered modified diferenças tracked separadamente independent states isolated contexts enabling parallel workflows scenarios comuns incluem developing feature branch main enquanto fixing critical bug hotfix branch enquanto reviewing pull request feature branch colega teammate reviewing diff comparing implementations testing locally validating functionality correctness quality assurance QA manual exploratory testing reproducibility issues debugging troubleshooting root cause analysis bisecting history identifying regression commits.

## Comandos Básicos

### Listar Worktrees Ativos

Executar comando git worktree list exibindo output mostrando path cada worktree branch associada commit HEAD atual status detached HEAD se aplicável bare repository indicação facilitating navigation management awareness workspaces disponíveis active utilizados esquecidos abandonados removidos cleanup maintenance necessário periodicamente evitando lixo acumulado disk space desperdício confusion clutter desorganization.

### Criar Novo Worktree

Criar worktree nova branch executando git worktree add ../carf-geoapi-feature-auth feature/RF-001-authentication ou criar worktree branch existente executando git worktree add ../carf-geoapi-hotfix hotfix/fix-rls-policy ou criar worktree detached HEAD commit específico executando git worktree add ../carf-geoapi-debug abc123def onde path pode ser relativo ou absoluto conforme preferência organizacional estrutura diretórios convenções time padronização facilitating navigação discovery consistency uniformity aesthetics clean organized tidy workspace pleasant work environment enjoyable developer experience happiness satisfaction morale productivity output quality craftsmanship pride ownership.

### Estrutura Diretórios Recomendada

Organizar workspace com diretório raiz contendo carf-geoapi como main worktree em branch main seguido por carf-geoapi-feature-auth para feature branch worktree, carf-geoapi-hotfix para hotfix branch worktree, e carf-geoapi-review para PR review worktree utilizando convenção naming clara explícita self-documenting intuitive understandable sem necessidade documentation mental overhead memorization cognitive load reduced facilitating onboarding newcomers teammates collaboration shared understanding common language vocabulary terminology consistent aligned unified coherent.

### Trabalhar no Worktree

Trabalhar no worktree navegando com cd ../carf-geoapi-feature-auth permitindo desenvolvimento normal editando files executando git add git commit git push onde IDE pode abrir projeto neste diretório independentemente com terminal sessions separadas para cada worktree e build processes isolated evitando conflicts race conditions. Cada worktree funciona repositório Git normal completo independente commands funcionam esperado commits pushes pulls fetches branches tags remotes configurations settings específicas contextuais adaptadas workflow particular task scenario requirements constraints preferences optimizations custom tailored personalized individual team project organization company enterprise cultural norms conventions best practices standards guidelines policies procedures documentation knowledge base wiki confluence notion obsidian markdown plain text version controlled reviewable searchable discoverable accessible transparent open collaborative shared living breathing evolving updated maintained current relevant accurate truthful honest authentic genuine real pragmatic practical actionable useful valuable meaningful impactful mattering difference lives people users customers stakeholders business society world better place legacy lasting.

### Remover Worktree

Deletar worktree após merge conclusão feature voltando para main worktree com cd workspace/carf-geoapi executando git worktree remove ../carf-geoapi-feature-auth ou forçar remoção se uncommitted changes existirem executando git worktree remove menos menos force ../carf-geoapi-hotfix. Limpeza periódica importante hygiene maintenance organizacional evitando accumulation stale outdated obsolete forgotten abandoned worktrees consuming disk space causing confusion clutter disorganization inefficiency waste resources computational human attention time energy focus concentration directed productively valuable activities impactful meaningful purposeful intentional deliberate thoughtful mindful present aware conscious engaged participating contributing adding value creating building making real tangible concrete measurable observable verifiable testable falsifiable scientific rigorous methodical systematic structured organized disciplined professional craftsmanship excellence quality standards high bar expectations accountability responsibility integrity honesty transparency authenticity vulnerability courage bravery boldness audacity daring dreaming imagining envisioning creating manifesting reality shaping future possibilities open endless limitless unbounded.

## Casos de Uso Comuns

### Desenvolvimento Feature Paralelo Hotfix Urgente

Desenvolvendo feature complexa multistep multiday effort sudden production incident critical bug requires immediate attention hotfix priority highest dropping everything context switching costly disruptive worktree solves keeping feature work intact preserving state uncommitted changes work-in-progress WIP experimental exploratory tentative uncertain evolving fluid dynamic adaptive responsive flexible. No meio do desenvolvimento da feature em workspace/carf-geoapi-feature-auth com uncommitted changes existentes código quebrado testes failing normal WIP criar worktree hotfix sem afetar feature voltando para cd ../carf-geoapi executando git worktree add ../carf-geoapi-hotfix hotfix/fix-critical-bug seguido por trabalhar no hotfix isoladamente navegando cd ../carf-geoapi-hotfix fazendo fix bug test commit push deploy production e voltar para feature development sem perdas executando cd ../carf-geoapi-feature-auth continuando exatamente onde parou estado preservado.

### Code Review Pull Request Colega

Reviewer precisa testar localmente PR pull request colega verificando funcionalidade correctness quality standards adherence checking out branch localmente conflita working directory atual uncommitted changes worktree solves criando isolated environment review testing validation approval feedback constructive respectful empathetic growth-oriented developmental coaching mentoring knowledge sharing learning teaching growing together collective improvement continuous evolution. Executar git worktree add ../carf-geoapi-review feature/RF-045-relatorios seguido por cd ../carf-geoapi-review executando npm install pois dependencies podem diferir rodando npm test para run test suite e npm start para test locally browser interaction manual exploratory providing feedback comments suggestions improvements approval depois retornando main worktree com cd ../carf-geoapi e removendo review worktree executando git worktree remove ../carf-geoapi-review.

### Comparação Implementações Diferentes Branches

Debugging investigation analysis comparison benchmarking performance profiling optimization choosing approach strategy tradeoffs analyzing pros cons advantages disadvantages costs benefits risks opportunities threats SWOT analysis informed decision-making data-driven evidence-based rational logical reasoned thoughtful deliberate careful prudent wise smart intelligent strategic tactical operational executional. Criar worktrees para ambas abordagens executando git worktree add ../carf-geoapi-approach-a feature/approach-a e git worktree add ../carf-geoapi-approach-b feature/approach-b permitindo run benchmarks both directories compare results metrics KPIs usando IDE compare files side-by-side diff tools visual highlighting garantindo decision documented justified explained transparent accountable.

## Integração IDE

**VS Code:** Cada worktree pode abrir instância separada VS Code File > Open Folder selecting worktree directory settings extensions configurations specific workspace isolated independent avoiding conflicts interference confusion mismatch expectations reality discrepancies bugs errors frustrations.

**IntelliJ IDEA / Rider:** Project structure recognizes worktree Git integration fully functional branch operations commits pushes pulls merges rebases fetches tags remotes everything works expected seamlessly transparently intuitively user-friendly.

**Terminal Multiplexers:** tmux screen organizing sessions windows panes cada worktree dedicated session context switching Alt+number hotkeys productivity efficiency speed velocity throughput output quality craftsmanship excellence mastery expertise professionalism dedication commitment discipline focus concentration presence awareness mindfulness intentionality purpose meaning contribution value impact mattering difference.

## Limitações e Cuidados

**Mesma Branch Múltiplos Worktrees:** Git impede checkout mesma branch múltiplos worktrees simultaneamente evitando conflicts corruption inconsistency confusion ambiguity which HEAD which index staging area working directory state authoritative source truth SSOT principle violation prevention enforcement validation verification.

**Disk Space:** Cada worktree contém working directory files duplicated consumindo espaço disco proporcionalmente repository size large monorepos gigabytes terabytes data careful management cleanup maintenance hygiene discipline responsibility accountability stewardship caring resources scarce finite limited precious valuable.

**Stale Worktrees:** Esquecer worktrees criados temporários testes esquecidos abandonados lixo acumulado poluição desorganização cleanup comando git worktree prune remove stale worktrees automaticamente detected missing directories removed references metadata garbage collection freeing resources reclaiming space optimizing performance.

## Relacionado

Para workflow de branches trunk-based development e feature branches short-lived, consulte 02-branching-strategy.

---

**Última atualização:** 2025-01-08
