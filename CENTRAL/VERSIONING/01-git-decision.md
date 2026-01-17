# Decisão Git - Sistema Controle Versão

Sistema controle versão escolhido para CARF é Git ferramenta distribuída open-source amplamente adotada indústria permitindo versionamento código rastreamento mudanças histórico completo commits branches merges colaboração time desenvolvimento coordenação trabalho paralelo features independentes isolation contextos merge estratégias fast-forward squash rebase mantendo histórico limpo legível compreensível. Git habilita workflow polyrepo estratégia cinco repositórios independentes GEOAPI GEOWEB REURBCAD GEOGIS WEBDOCS cada um versionado autonomamente releases coordenadas compatibilidade cruzada documentada release notes especificando versões compatíveis entre projetos garantindo integração funcionamento correto sistema completo evitando breaking changes incompatibilidades runtime deployment failures.

## Justificativa Escolha Git

Git escolhido versus alternativas Mercurial SVN Subversion Perforce CVS devido performance superior operações locais branching merging extremamente rápidos suporte robusto workflows distribuídos offline-first desenvolvedores trabalham localmente sem conexão servidor central committam localmente synchronizam posteriormente quando conectividade disponível. Ecossistema rico ferramentas GUI clients SourceTree GitKraken GitHub Desktop Sublime Merge integração IDEs VS Code Visual Studio IntelliJ Rider Eclipse facilitando adoção onboarding desenvolvedores novos familiaridade prévia portabilidade skills mercado trabalho competências transferíveis. Documentação extensa comunidade massiva Stack Overflow GitHub Discussions tutoriais cursos bootcamps facilitando troubleshooting resolução problemas aprendizado contínuo best practices convenções padrões estabelecidos industry-wide Gitflow GitHub Flow trunk-based development adaptáveis contextos equipes tamanhos diferentes startups enterprises.

## Alternativas Consideradas

**Mercurial:** Similar Git distribuído porém ecossistema menor comunidade reduzida ferramentas limitadas adoption declining empresas migrando Git preferência mercado. **SVN Subversion:** Centralizado single point of failure servidor offline bloqueia commits performance inferior branching custoso histórico servidor não local impedindo work offline portabilidade limitada. **Perforce:** Enterprise-grade performático arquivos binários grandes gaming assets porém licenciado custo alto overkill projeto CARF predominantemente texto código configuração markdown SQL migrations. **CVS:** Legado obsoleto deficiências críticas atomic commits file-level tracking inadequado projetos modernos.

## Configurações Recomendadas

Configuração global Git incluindo user.name user.email core.autocrlf input evitando problemas line endings cross-platform Windows Linux macOS core.editor configurado preferência pessoal VSCode vim nano pull.rebase true mantendo histórico linear evitando merge commits desnecessários fetch.prune true limpando branches remotas deletadas init.defaultBranch main convenção moderna substituindo master terminology inclusive. Aliases úteis git config --global alias.st status git config --global alias.co checkout git config --global alias.br branch git config --global alias.lg "log --oneline --graph --decorate --all" visualizando histórico gráfico compacto. Git LFS Large File Storage configurado repositórios contendo assets binários ortofotos shapefiles GeoTIFF rasters evitando bloat repositório performance degradation clones lentos storage eficiente pointer files server-side binary storage.

## Integração CI/CD

Git integrado GitHub Actions workflows CI/CD pipelines triggered push eventos branches específicas main develop feature/* release/* tags v*.*.* semantic versioning pattern executando automaticamente build test lint coverage quality gates security scans SAST dependency vulnerabilities Snyk Dependabot deploy staging production environments approval gates manual interventions critical releases. Webhooks notificações Slack Discord Microsoft Teams alertando time eventos importantes pull requests opened reviews requested approved merged deployments succeeded failed incidents detected rollback triggered restoring previous stable version blue-green deployment strategy zero downtime.

## Treinamento Time

Onboarding desenvolvedores novos inclui Git fundamentals workshop 2 horas conceitos básicos repository clone staging area commit history branches merging conflicts resolution hands-on exercises práticos simulando cenários reais. Advanced topics session 1 hora rebasing interactive rebase squashing commits cherry-picking stashing reflog recovering lost commits bisect debugging identifying regression commits blame authorship file changes hooks automation pre-commit lint staged post-commit notifications. Resources disponíveis Pro Git book online gratuito comprehensive Atlassian Git tutorials visual interactive learning Oh My Git game gamification concepts practice safe environment mistakes encouraged learning experimentation growth mindset.

---

**Última atualização:** 2025-01-08
**Status do arquivo**: Review
