---
modules: [GEOWEB]
epic: scalability
---

# UC-006: Gerar Relatório de Comunidade

Caso de uso permitindo usuários autorizados (MANAGER com permissão reports.read para relatórios gerenciais, ADMIN com acesso total ao tenant) gerarem relatório consolidado com estatísticas completas e visualizações de uma comunidade após autenticação e seleção de comunidade com dados cadastrados, onde fluxo principal inicia com acesso ao menu Relatórios exibindo tipos disponíveis incluindo Relatório de Comunidade Relatório de Legitimação Relatório de Equipes, usuário seleciona Relatório de Comunidade abrindo formulário de parâmetros contendo dropdown de comunidades listando todas communities do tenant ordenadas alfabeticamente, seletor de período com data início e data fim para filtrar unidades criadas ou modificadas no intervalo, checkboxes de seções a incluir permitindo customizar conteúdo (Estatísticas Gerais mostrando totais e agregações, Distribuição de Unidades por Status com gráfico de pizza, Estatísticas de Titulares com médias e contagens, Mapa de Situação renderizando geometrias coloridas por status, Lista de Unidades com tabela paginada de todas unidades), e radio buttons de formato de saída oferecendo PDF para visualização profissional Excel para análise de dados CSV para importação externa, usuário preenche parâmetros selecionando comunidade definindo período marcando seções desejadas escolhendo formato e clica botão Gerar Relatório disparando validação verificando comunidade selecionada não null, período válido com data_inicio ≤ data_fim, ao menos uma seção marcada, se validação passa sistema inicia geração assíncrona criando job em background usando BullMQ adicionando à fila reports-queue com payload JSON contendo user_id community_id date_range sections format, exibe mensagem toast azul "Relatório sendo gerado. Você será notificado quando estiver pronto" e retorna usuário para dashboard, worker dedicado consome job da fila executando processamento busca dados da comunidade via query SELECT com JOINs incluindo units holders unit_holders aplicando filtros WHERE community_id = $id AND created_at BETWEEN $start AND $end, calcula estatísticas agregando total de unidades agrupadas por status usando COUNT GROUP BY, área total cadastrada somando area_m2 via SUM, total de titulares únicos contando DISTINCT holder_id, distribuição por tipo de unidade agrupando type, gera gráficos usando Chart.js renderizando canvas em Node.js criando pie chart para status bar chart para tipos, gera mapa estático capturando screenshot do mapa web usando Puppeteer navegando URL do frontend com geometrias e salvando PNG, renderiza template HTML de relatório usando Handlebars injetando dados calculados e imagens geradas, converte HTML para PDF usando Puppeteer com page.pdf() configurando formato A4 orientação portrait margens 1cm ou converte para Excel usando ExcelJS criando workbook com múltiplas sheets uma por seção populando células com dados tabulares e aplicando estilos headers bold, salva arquivo gerado em object storage (AWS S3 Azure Blob) em bucket reports/ com key gerada report_{community_id}_{timestamp}.pdf garantindo unicidade, gera URL presigned com TTL 24 horas permitindo download temporário sem autenticação adicional evitando expor bucket público, marca job como completed atualizando status em BullMQ, sistema envia notificação push ao usuário via WebSocket ou email dependendo de preferências mostrando "Relatório pronto para download" com link clicável, usuário clica em notificação abrindo página de download exibindo preview embutido se PDF usando iframe com src apontando para presigned_url ou botão Download direto se Excel, usuário clica Baixar iniciando download do arquivo salvando localmente com nome descritivo Relatorio_Comunidade_Vila_Nova_2025-12-30.pdf permitindo impressão compartilhamento arquivamento. Fluxos alternativos incluem geração rápida síncrona para comunidades pequenas <100 unidades (UC-006-FA-001) e agendamento de envio recorrente com cron job (UC-006-FA-002). Fluxos de exceção cobrem timeout de geração excedendo 10 minutos (UC-006-FE-001), dados insuficientes quando comunidade sem unidades (UC-006-FE-002), e erro ao gerar PDF com fallback para HTML (UC-006-FE-003).

**Fluxos Alternativos:**
- UC-006-FA-001: Geração rápida (poucos dados)
- UC-006-FA-002: Agendar geração recorrente

**Fluxos de Exceção:**
- UC-006-FE-001: Timeout de geração
- UC-006-FE-002: Dados insuficientes
- UC-006-FE-003: Erro ao gerar PDF

**Regras de Negócio:**
- RN-001: Relatórios grandes (>1000 unidades) sempre gerados assincronamente via BullMQ
- RN-002: URL presigned expira em 24h exigindo nova geração após expiração
- RN-003: Usuário limitado a 5 relatórios pendentes simultâneos prevenindo sobrecarga de fila
- RN-004: Arquivos de relatórios deletados automaticamente após 30 dias economizando storage
- RN-005: Apenas MANAGER e ADMIN podem agendar relatórios recorrentes (ANALYST somente sob demanda)

**Rastreabilidade:**
- RF-203, RF-204, RF-205, RF-207, RF-209
- US-074, US-075

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
