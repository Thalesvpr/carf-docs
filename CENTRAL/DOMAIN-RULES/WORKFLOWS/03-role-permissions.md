---
type: leaf
status: approved
updated: 2026-01-25
---

# Role Permissions

Sistema RBAC com cinco niveis hierarquicos de autorizacao. SUPER_ADMIN possui acesso irrestrito incluindo configuracoes criticas e manipulacao de logs. ADMIN gerencia usuarios, times e configuracoes operacionais do tenant. MANAGER aprova unidades, gerencia processos de legitimacao e emite certidoes. ANALYST revisa e recomenda aprovacao sem poder aprovar definitivamente. FIELD_AGENT cadastra unidades e titulares em modo rascunho.

Segregacao de responsabilidades exige dupla verificacao em decisoes criticas. Analyst revisa, Manager aprova. Emissao de certidao requer permissoes units.approve, legitimation.approve e documents.generate simultaneamente.

## Politicas de Atribuicao

Novos usuarios recebem FIELD_AGENT por padrao. Promocao para ANALYST requer aprovacao de MANAGER e capacitacao em analise tecnica. Promocao para MANAGER requer ADMIN e historico minimo de 6 meses com taxa de aprovacao superior a 95%. Role ADMIN restrito a funcionarios efetivos do orgao publico. SUPER_ADMIN exclusivo para equipe tecnica de infraestrutura.

Auditoria registra todas execucoes de acoes sensiveis incluindo usuario, IP, timestamp, parametros e resultado. Tentativas de acesso negado geram alertas de seguranca.
