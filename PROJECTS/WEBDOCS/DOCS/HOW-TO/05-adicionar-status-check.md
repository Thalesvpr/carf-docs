# Adicionar Status Check

Guia para incluir novo serviço na status page permitindo monitorar disponibilidade.

Identificar endpoint de health do serviço a monitorar. Endpoint deve retornar HTTP 200 quando serviço está saudável e código de erro quando não está. Response pode incluir detalhes em JSON mas não é obrigatório.

Editar arquivo de configuração em src/config/services.ts que define array de serviços monitorados. Cada serviço tem id único usado internamente, name para exibição na interface, url do endpoint de health, e timeout em milissegundos.

Adicionar entrada para novo serviço com id descritivo em kebab-case, name legível para usuários, url completa do endpoint de health, e timeout apropriado (5000ms padrão, aumentar para serviços lentos).

Testar localmente executando bun run dev e acessando /status/. Novo serviço deve aparecer na lista com indicador de status. Verificar que status reflete corretamente disponibilidade do serviço.

Configurar variável de ambiente se URL do serviço diferir entre ambientes. Usar process.env para ler variável em services.ts. Adicionar variável em .env.example com valor de exemplo e documentar.

Considerar autenticação se endpoint de health requer token. Status page executa fetch server-side então token pode ser incluído em header sem expor ao cliente. Armazenar token em variável de ambiente.

Commit e push da mudança. Pipeline de CI valida build. Preview deployment permite testar em ambiente similar a produção antes de merge.

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
