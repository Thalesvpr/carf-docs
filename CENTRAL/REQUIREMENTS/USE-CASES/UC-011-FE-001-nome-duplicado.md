---
modules: [GEOWEB, REURBCAD]
epic: teams
---

# UC-011-FE-001: Nome de Equipe Duplicado

Fluxo de exceção do UC-011 Gerenciar Equipes Técnicas ocorrendo no passo 7 durante validação quando sistema verifica unicidade de nome executando query SELECT COUNT(*) FROM teams WHERE name = $name AND tenant_id = $tenant retornando count > 0 indicando já existe equipe com mesmo nome, tipicamente causado por ADMIN tentando criar "Equipe Zona Norte" mas já existe equipe ativa ou inativa com exato mesmo nome causando violação de constraint UNIQUE, sistema detecta duplicata antes de tentar INSERT evitando exception de banco, exibe modal vermelho erro com ícone de alerta título "Nome Duplicado" mensagem "Já existe uma equipe com o nome 'Equipe Zona Norte'. Escolha um nome diferente ou verifique equipes inativas" orientando usuário, mantém formulário aberto com dados preenchidos preservando informações já digitadas evitando retrabalho, foco retorna automaticamente para campo Nome da Equipe destacado com borda vermelha indicando campo problemático, usuário ajusta nome para variante única como "Equipe Zona Norte - Levantamento 2025" ou "Equipe Norte A" diferenciando de equipe existente, clica Criar Equipe novamente executando validação que agora passa retornando count = 0 prosseguindo normalmente, alternativamente usuário pode clicar link "ver equipes existentes" embutido na mensagem de erro abrindo listagem filtrada para verificar equipes com nomes similares incluindo inativas identificando possível equipe antiga que poderia ser reativada ao invés de criar nova duplicando estrutura organizacional desnecessariamente.

**Ponto de Desvio:** Passo 7 do UC-011 (validação antes de INSERT)

**Retorno:** Criação bloqueada, usuário altera nome e retenta

---

**Última atualização:** 2025-12-30
