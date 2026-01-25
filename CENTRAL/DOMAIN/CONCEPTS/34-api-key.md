---
type: leaf
status: approved
updated: 2026-01-24
---

# Chave de API

Credencial para autenticacao de integracoes automatizadas. Permite que scripts, plugins GIS, e sistemas externos acessem API sem login interativo.

Chaves de API sao alternativa ao login OAuth2 para integracao maquina-a-maquina. Plugin QGIS usa chave para sincronizar dados. Script noturno usa chave para gerar relatorios.

## Permissoes

Cada chave tem escopo de permissoes definido. Principio de privilegio minimo - chave recebe apenas acessos estritamente necessarios para sua funcao.

## Seguranca

Valor completo da chave e exibido apenas uma vez na criacao. Sistema armazena apenas hash criptografico. Chave perdida nao pode ser recuperada - nova deve ser criada.

## Rastreabilidade

Sistema registra quando chave foi usada pela ultima vez e total de requisicoes. Permite identificar chaves abandonadas ou uso anormal indicando possivel comprometimento.

## Revogacao

Chave pode ser desativada a qualquer momento invalidando imediatamente acessos. Util quando integracao e descontinuada ou suspeita-se de vazamento.
