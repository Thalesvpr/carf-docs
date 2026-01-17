---
modules: [GEOWEB]
epic: performance
---

# UC-006-FE-003: Erro ao Gerar PDF

Fluxo de exceção do UC-006 Gerar Relatório de Comunidade ocorrendo no passo 11.6 durante conversão de HTML para PDF quando Puppeteer tenta executar page.pdf() mas falha lançando exceção tipicamente causada por timeout de renderização com página HTML complexa contendo SVGs pesados de gráficos e mapas excedendo limite de processamento, falta de fontes instaladas no servidor headless Chrome não encontrando Roboto ou Arial especificadas no CSS resultando em texto ilegível, ou crash do processo Chromium por out-of-memory em servidor com RAM limitada ao processar imagens grandes de mapas, sistema captura exceção em bloco try-catch envolvendo await page.pdf() logando erro completo com stack trace no sistema de logging (Winston ou similar) com level error e tags puppeteer pdf-generation para facilitar troubleshooting, implementa retry automático executando nova tentativa com timeout aumentado de 30s para 60s e configuração reduceMemory: true no Puppeteer launch otimizando consumo de recursos, se segunda tentativa também falha sistema desiste de geração PDF aborta conversão mas não descarta trabalho já realizado mantendo template HTML renderizado com dados calculados gráficos embutidos como base64 e estilos CSS inline, salva arquivo HTML em object storage com mesma estrutura de path reports/{community_id}_{timestamp}.html gerando presigned URL válida por 24h permitindo acesso temporário, marca job como completed_with_warnings ao invés de failed pois relatório foi gerado apenas em formato alternativo, envia notificação ao usuário com ícone amarelo warning título "Relatório Disponível em HTML" mensagem "Houve um erro ao gerar o PDF. O relatório foi salvo em formato HTML como alternativa. Você pode visualizá-lo no navegador ou tentar gerar novamente em PDF" com botões Baixar HTML abrindo presigned_url em nova aba e Tentar PDF Novamente reenfileirando job com mesmos parâmetros, HTML gerado mantém fidelidade visual completa com gráficos interativos usando Chart.js funcionais permitindo hover para ver valores exatos e mapa renderizado como imagem estática PNG garantindo usuário não perde acesso aos dados apenas formato final é diferente, e sistema registra métrica de falha em dashboard de observabilidade alertando equipe técnica sobre problema recorrente que pode indicar necessidade de upgrade de infraestrutura ou otimização de templates.

**Ponto de Desvio:** Passo 11.6 do UC-006 (conversão para PDF falha)

**Retorno:** HTML salvo como fallback, usuário pode baixar ou retentar PDF

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
