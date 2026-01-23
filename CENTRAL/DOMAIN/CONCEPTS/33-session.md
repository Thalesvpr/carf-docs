---
type: leaf
status: review
updated: 2026-01-22
---

# Sessao

Registro de usuario autenticado no sistema. Rastreia token de acesso, dispositivo usado, e tempo de atividade para gerenciamento de acessos.

Cada login bem-sucedido cria uma sessao. Usuario pode ter multiplas sessoes simultaneas - computador do trabalho, celular, tablet. Cada uma e gerenciada independentemente.

## Token

Identificador unico da sessao usado para autenticar requisicoes. Armazenado em formato hash para seguranca - mesmo que banco seja comprometido, tokens nao sao expostos.

## Metadados

Registra endereco IP e identificacao do navegador ou aplicativo. Permite auditoria de acessos e deteccao de atividade suspeita - login de localizacao inesperada.

## Expiracao

Sessoes tem tempo de vida limitado. Access token curto (15 minutos) e renovado automaticamente. Inatividade prolongada exige nova autenticacao.

## Logout

Usuario pode encerrar sessoes individualmente ou todas de uma vez. Administrador pode forcar logout remotamente em caso de suspeita de comprometimento.
