---
type: leaf
status: approved
updated: 2026-02-07
---

# Conflict Resolution

Algoritmo completo de deteccao e resolucao de conflitos durante sincronizacao entre o app mobile REURBCAD e o servidor GEOAPI. Conflitos ocorrem quando o mesmo registro e modificado por diferentes usuarios ou dispositivos durante o periodo em que o app opera offline.

## Deteccao de Conflito

A deteccao acontece durante o push de dados locais para o servidor. Cada registro no app possui um campo version que reflete a versao do registro no momento da ultima sincronizacao. Ao enviar uma operacao de update para o servidor, o payload inclui essa version. O servidor compara a version recebida com a version atual do registro no banco PostgreSQL. Se a version do servidor for maior que a enviada pelo client, significa que outro usuario ou dispositivo modificou o registro desde a ultima sincronizacao do app, configurando um conflito.

Para operacoes de create, nao ha conflito de versao pois o registro e novo. O servidor atribui server_id e version 1, retornando esses valores ao client. Para operacoes de delete, o servidor aceita a exclusao se a version coincidir. Se nao coincidir, trata como conflito de delete-versus-update.

## Estrategia Padrao: Last-Write-Wins por Campo

A estrategia padrao e last-write-wins aplicada por campo individual, nao por registro inteiro. Isso minimiza a perda de dados quando duas pessoas editam o mesmo registro mas campos diferentes.

Quando conflito e detectado, o servidor compara campo a campo os valores do registro local (enviado pelo client) e do registro atual no servidor. Para cada campo, tres cenarios sao possiveis. Se apenas o client modificou o campo em relacao a versao base, o servidor aceita o valor do client. Se apenas o servidor tem valor diferente da versao base (outro usuario modificou), o servidor mantem seu valor. Se ambos modificaram o mesmo campo (valor do client e valor do servidor sao ambos diferentes da versao base), o sistema gera um registro de conflito especifico para aquele campo.

## Resolucao de Conflito

Para campos onde ambos os lados divergem, o servidor retorna na response do push um objeto conflictData contendo, para cada campo divergente, o valor local (clientValue) e o valor do servidor (serverValue). O app recebe esses dados e exibe um dialogo de resolucao ao usuario.

O dialogo mostra os campos conflitantes lado a lado: nome do campo na esquerda, valor local (o que o usuario digitou) no centro-esquerda com indicacao "Sua versao", valor do servidor no centro-direita com indicacao "Versao do servidor". O usuario seleciona campo a campo qual valor manter. Apos resolver todos os campos, o app envia o registro merged ao servidor com a version incrementada.

Se o usuario nao resolver o conflito imediatamente, o registro permanece na fila de conflitos pendentes, acessivel via tela de configuracoes na secao de sincronizacao. O indicador de conflitos pendentes e visivel na barra de status do app.

## Casos Especiais

Delete versus update: quando o servidor deletou o registro e o client editou, o dialogo pergunta ao usuario se deseja manter sua versao local (recriando o registro no servidor) ou aceitar a exclusao (descartando suas edicoes locais). Quando o client deletou e o servidor editou, o sistema aceita a exclusao do client pois a intencao de deletar e considerada mais forte que a edicao.

Fotos nunca conflitam pois seguem padrao append-only. Fotos capturadas localmente sempre sobem ao servidor como novos registros de documento. Fotos que existem no servidor sempre baixam ao dispositivo durante pull. Nao ha substituicao ou exclusao cruzada de fotos. Se dois dispositivos tiraram fotos diferentes da mesma unidade, ambas sao preservadas como documentos distintos.

Campos de geometry (coordenadas de boundary) sao tratados como campo atomico: se ambos lados modificaram a geometria, o conflito e mostrado ao usuario para escolha, pois merge automatico de poligonos nao faz sentido geometrico.

## Retry Apos Resolucao

Apos resolucao de conflito pelo usuario, o app reenvia o registro merged com version incrementada para a version atual do servidor mais 1. Se entre a resolucao e o reenvio outro usuario modificou o mesmo registro novamente (cenario raro), um novo conflito sera detectado e o processo se repete. Na pratica, isso quase nunca acontece pois equipes de campo trabalham em comunidades diferentes com pouca sobreposicao de dados.

## Metricas

O app rastreia localmente: numero de conflitos detectados por sessao de sync, tempo medio de resolucao por conflito, campos mais frequentemente conflitantes. Esses dados sao enviados ao servidor como telemetria anonima para identificar padroes que possam indicar problemas de processo (duas equipes trabalhando na mesma comunidade sem coordenacao).
