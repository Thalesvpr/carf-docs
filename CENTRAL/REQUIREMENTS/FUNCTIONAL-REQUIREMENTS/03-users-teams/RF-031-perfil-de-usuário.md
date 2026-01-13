---
modules: [GEOWEB]
epic: authentication
---

# RF-031: Perfil de Usuário

Usuário autenticado pode visualizar e editar seu próprio perfil onde exibição inclui informações básicas como nome completo email role atribuída tenant vinculado data de criação da conta último acesso e estatísticas de uso (quantidade de unidades cadastradas documentos anexados), edição de foto de perfil implementada com upload de imagem validando formato (JPEG PNG) e tamanho máximo (ex: 2MB) aplicando redimensionamento automático para dimensões padronizadas (ex: 200x200 pixels) e armazenamento em storage de objetos (S3 Azure Blob) com URL acessível via CDN, alteração de senha própria disponível através de formulário seguro validando senha atual antes de permitir definição de nova senha exigindo conformidade com política de complexidade (mínimo 8 caracteres 1 maiúscula 1 minúscula 1 número 1 caractere especial) e sincronizando mudança com Keycloak, implementação em módulo GEOWEB com página dedicada de perfil controles de edição inline preview de foto antes de upload validações em tempo real e feedback de salvamento bem-sucedido.

---

**Última atualização:** 2025-12-30
