---
modules: [GEOWEB]
epic: holders
---

# RF-195: Indicador de Pendências

O sistema exibe indicador visual proeminente de pendências de sincronização através de badge numérico apresentado sobre ícone de sincronização na interface principal do aplicativo, mostrando quantidade total de registros locais que foram criados ou modificados mas ainda não foram transmitidos ao servidor central. Ao tocar no indicador, usuário acessa listagem detalhada de registros pendentes organizada por tipo de entidade (unidades, titulares, fotos, etc.) e tipo de operação (criação, edição, deleção), incluindo identificação de cada registro como nome da unidade ou titular afetado, facilitando compreensão de exatamente quais dados aguardam sincronização. O contador de pendências é atualizado em tempo real sempre que usuário cria novo registro, edita registro existente ou completa sincronização bem-sucedida, garantindo que indicador reflita sempre estado atual preciso de dados não sincronizados sem necessidade de recarregar aplicativo. Este indicador visual serve função crítica de awareness situacional, lembrando constantemente usuário sobre existência de trabalho local não persistido no servidor e motivando execução de sincronização assim que conectividade estiver disponível, reduzindo risco de perda de dados por esquecimento de sincronizar antes de desinstalar aplicativo, trocar de dispositivo ou executar reset de fábrica.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
