# Deploy para Vercel

Guia para configurar e executar deploy do WEBDOCS na plataforma Vercel.

Conectar repositório GitHub ao Vercel via dashboard. Criar novo projeto selecionando repositório do WEBDOCS. Vercel detecta automaticamente framework Astro e configura build settings padrão.

Configurar settings de build em project settings ou vercel.json. Framework preset Astro, build command bun run build, output directory dist, e install command bun install. Root directory apontando para SRC-CODE/carf-webdocs se repositório é monorepo.

Configurar variáveis de ambiente no dashboard Vercel em Settings > Environment Variables. Adicionar todas variáveis de .env.example com valores de produção. Marcar variáveis sensíveis como sensitive para ocultar valores em logs.

Configurar domínio customizado em Settings > Domains. Adicionar domínio e configurar DNS conforme instruções do Vercel. Certificado SSL provisionado automaticamente via Let's Encrypt.

Deploy automático acontece em push para branch main. Vercel detecta push via webhook, executa build, e deploya para produção se bem-sucedido. Rollback automático se health check falhar após deploy.

Preview deployments criados automaticamente para pull requests. URL única por PR permite review de mudanças. Comments automáticos no PR linkam para preview. Útil para validar mudanças de conteúdo e código antes de merge.

Monitorar deploys no dashboard Vercel em Deployments. Logs de build disponíveis para debug de falhas. Analytics mostram métricas de performance e uso. Alertas configuráveis para falhas de deploy ou degradação de performance.

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
