---
modules: [GEOWEB, REURBCAD]
epic: holders
---

# UC-003-FE-003: Soma de Percentuais > 100%

Fluxo de exceção do UC-003 Vincular Titular a Unidade ocorrendo na validação quando soma de ownership_percentage de todos titulares da unidade incluindo novo vínculo ultrapassa 100%, onde validação calcula `SELECT SUM(ownership_percentage) FROM unit_holders WHERE unit_id = $1 AND deleted_at IS NULL` adicionando percentual informado no formulário verificando se total > 100. Sistema ao detectar excedente retorna HTTP 400 Bad Request com body contendo soma atual (ex: 85%), percentual tentando adicionar (ex: 30%), total resultante (115%), e sugestão de percentual máximo permitido (15% = 100% - 85%), frontend exibe modal de warning com título "Percentuais Ultrapassam 100%" apresentando cálculo visual "85% (titulares atuais) + 30% (novo) = 115% > 100%" destacando excedente em vermelho, lista titulares atuais com percentuais mostrando quem já possui quanto facilitando decisão de ajuste, e oferece ações: Ajustar Automaticamente calculando percentual máximo permitido (100% - soma_atual) preenchendo automaticamente campo com valor seguro, Editar Manualmente mantendo modal aberto com campo percentual focado permitindo usuário digitar valor correto entre 0-15%, ou Redistribuir Percentuais abrindo tela avançada mostrando todos titulares com sliders permitindo ajustar proporcionalmente mantendo soma = 100%.

**Ponto de Desvio:** Validação antes de criar vínculo (soma ultrapassa 100%)

**Cálculo de Excedente:**

Backend executa query await db com tabela unit_holders aplicando where com unit_id igual unitId e deleted_at null agregando sum com ownership_percentage as total finalizando com first() armazenando em currentSum, converte formData.ownership_percentage para float usando parseFloat armazenando em newPercentage, calcula totalAfter somando currentSum.total ou zero se nullable mais newPercentage, verifica condição if totalAfter maior cem calculando maxAllowed como cem menos currentSum.total ou zero, lançando ValidationError com field igual ownership_percentage message interpolada "Soma ultrapassa 100%. Máximo permitido: ${maxAllowed}%" e details contendo current_sum igual soma atual attempting_to_add igual percentual novo total_after igual total resultante e max_allowed igual percentual máximo permitido retornando HTTP 400 Bad Request com detalhes completos.

**Modal de Warning:**

Modal exibe ícone warning laranja com título "Percentuais Ultrapassam 100%" apresentando seção "Titulares atuais: X%" com lista de bullet points mostrando nome de cada titular percentual e tipo de relacionamento entre parênteses interpolando dados reais como João Silva cinquenta por cento Proprietário e Maria Souza trinta e cinco por cento Cônjuge, seguido por linha destacada "Tentando adicionar: Y%" com valor informado no formulário, linha resultado "Total: Z% ❌" com ícone X vermelho indicando erro, linha informativa "Máximo permitido: W%" calculado como cem menos soma atual, finalizando com quatro botões de ação sendo Ajustar para W% preenchendo automaticamente campo com valor seguro, Editar Manualmente mantendo foco no campo percentual, Redistribuir Todos abrindo tela avançada com sliders proporcionais, e Cancelar abortando operação.

**Retorno:** Usuário ajusta percentual e tenta novamente, ou cancela operação

---

**Última atualização:** 2025-12-30
