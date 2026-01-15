---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-123: Testar Conexao com Geoservico

Como Administrador quero testar conectividade com WMS para que possa validar configuracao de geoservicos antes de disponibiliza-los para usuarios finais, onde o endpoint implementado em GEOAPI expoe a rota /api/geoservices/{id}/test executando verificacao de conectividade e validacao de credenciais contra o servidor WMS configurado, garantindo que a operacao de teste nao impacte dados de producao realizando apenas requisicoes GetCapabilities sem alteracao de estado, permitindo deteccao de erros de configuracao incluindo URL invalida, credenciais incorretas, certificados SSL expirados, timeout de rede e servicos WMS fora do ar, incluindo validacao de permissoes baseada em roles onde apenas usuarios com role Administrator podem executar testes de conectividade, garantindo tratamento adequado de erros HTTP e de rede com mensagens descritivas que auxiliem o administrador a diagnosticar e corrigir problemas de configuracao, onde a resposta do endpoint inclui objeto TestResult com propriedades success message latency e capabilities contendo metadados do servico WMS quando a conexao for bem-sucedida, permitindo que o frontend GEOWEB exiba feedback visual imediato sobre o status da conexao incluindo icone de sucesso ou erro, tempo de resposta e lista de layers disponiveis no servico testado, garantindo rastreabilidade ao requisito funcional RF-217 que especifica a necessidade de validacao de geoservicos externos, incluindo testes unitarios que mockam respostas do servidor WMS simulando cenarios de sucesso timeout e autenticacao negada, onde a implementacao utiliza HttpClient com timeout reduzido para evitar bloqueio prolongado da thread em caso de servidores lentos, permitindo execucao assincrona do teste de conectividade retornando 202 Accepted com Location header para polling do resultado quando o teste demora mais de 5 segundos, garantindo que administradores possam re-testar geoservicos periodicamente para monitorar disponibilidade e performance dos servicos externos integrados.

---

**Ultima atualizacao:** 2025-12-30
**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
