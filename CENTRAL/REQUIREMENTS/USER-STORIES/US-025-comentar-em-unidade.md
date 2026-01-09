---
modules: [GEOAPI, REURBCAD]
epic: security
---

# US-025: Comentar em Unidade

Como analista, quero adicionar comentários em unidades para que equipe colabore, onde o sistema fornece canal de comunicação contextual permitindo que membros da equipe discutam, façam anotações e compartilhem informações diretamente no contexto de cada unidade, garantindo que conhecimento relevante e decisões são documentados junto ao registro apropriado. O cenário principal de uso ocorre quando um analista identifica necessidade de comunicar algo sobre uma unidade específica e adiciona comentário em seção dedicada na página de detalhes, permitindo escrever texto formatado usando markdown para estruturação de conteúdo, mencionar outros usuários através de notação @nome para chamar atenção de colegas específicos, e visualizar thread de comentários anteriores mantendo contexto da conversação. Os critérios de aceitação incluem capacidade de criar comentário com texto suportando formatação markdown incluindo negrito, itálico, listas e links para permitir comunicação rica e estruturada, funcionalidade de menção a usuários usando sintaxe @nome onde sistema autocompleta nomes de membros da equipe enquanto digita, envio de notificação automática para usuários mencionados alertando que foram referenciados em comentário com link direto para o contexto, e permissão para editar ou deletar apenas comentários próprios onde criador do comentário pode modificá-lo ou removê-lo mas comentários de outros usuários são protegidos. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoints POST /api/units/{id}/comments para criar comentário e GET /api/units/{id}/comments para listar, com sistema de notificações integrado) e GEOWEB (componente de comentários com editor markdown, autocomplete de menções e thread de discussão), garantindo rastreabilidade com RF-081 (Sistema de Comentários), onde comentários são associados permanentemente à unidade, marcados com timestamp e autor, incluem parsing de markdown no servidor para segurança, e notificações são entregues tanto in-app quanto opcionalmente por email para usuários mencionados.

---

**Última atualização:** 2025-12-30