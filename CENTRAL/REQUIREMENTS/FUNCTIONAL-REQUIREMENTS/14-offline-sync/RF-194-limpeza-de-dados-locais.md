---
modules: [REURBCAD]
epic: communities
---

# RF-194: Limpeza de Dados Locais

O sistema oferece funcionalidade de limpeza de cache que permite ao usuário liberar espaço de armazenamento do dispositivo móvel removendo dados sincronizados que não precisam mais estar disponíveis offline, especialmente útil quando técnico conclui trabalho em uma comunidade e prepara dispositivo para trabalhar em outra localidade. A opção de limpeza implementa lógica inteligente que preserva automaticamente dados não sincronizados, ou seja, registros criados ou editados localmente que ainda não foram transmitidos ao servidor, garantindo que trabalho pendente de sincronização nunca seja perdido inadvertidamente durante operação de limpeza. Antes de executar remoção efetiva, o sistema apresenta diálogo de confirmação obrigatória que alerta usuário sobre ação irreversível e lista quantos registros serão removidos e quanto espaço será liberado, incluindo advertência destacada sobre necessidade de ter sincronizado previamente todos os dados importantes, prevenindo limpezas acidentais que resultariam em perda de trabalho. Após confirmação, dados sincronizados são removidos do banco SQLite local e arquivos de mídia associados são deletados do sistema de arquivos, liberando espaço que pode ser reutilizado para download de dados de nova comunidade ou armazenamento de fotos e documentos coletados em trabalhos de campo subsequentes.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
