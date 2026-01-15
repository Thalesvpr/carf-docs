---
modules: [GEOAPI, GEOWEB, GEOGIS]
epic: security
---

# UC-010-FE-003: Layer Não Encontrado

Fluxo de exceção do UC-010 Configurar Camadas WMS ocorrendo no passo 8 quando sistema parseia XML GetCapabilities com sucesso mas não encontra nenhum elemento Layer listado indicando servidor WMS configurado incorretamente ou vazio tipicamente causado por servidor em modo de configuração inicial sem layers publicados ainda, permissões restritivas onde layers existem mas são privados não retornados em GetCapabilities público exigindo autenticação, ou filtro de capabilities mal configurado no servidor excluindo todos layers do XML response, sistema itera elementos buscando tags wms:Layer ou Layer dependendo de namespace verificando array de layers está vazio length === 0, detecta ausência exibindo modal amarelo warning com ícone de informação título "Nenhum Layer Disponível" mensagem "O servidor WMS respondeu corretamente mas não possui layers disponíveis para configuração. Possíveis causas: servidor sem dados publicados, layers requerem autenticação, ou URL aponta para serviço diferente de WMS" orientando sobre diagnóstico, inclui seção Verificações Sugeridas com checklist de ações como "Confirme URL com administrador do servidor WMS", "Verifique se servidor requer autenticação (usuário/senha ou API key)", "Teste URL em cliente desktop (QGIS) confirmando visibilidade de layers", botão Ver Capabilities Completo abrindo modal com XML formatado pretty-printed permitindo ADMIN inspecionar response completo verificando se realmente não há tags Layer ou se parsing falhou silenciosamente, botão Cancelar fechando modal e descartando configuração, se servidor requer autenticação ADMIN pode adicionar suporte futuro incluindo campos username password no formulário que sistema envia via HTTP Basic Auth no header Authorization ou API key como query param dependendo de especificação do servidor, alternativamente ADMIN pode contatar administrador do servidor WMS externo solicitando publicação de layers ou liberação de permissões para IP do servidor GEOAPI permitindo acesso via GetCapabilities público.

**Ponto de Desvio:** Passo 8 do UC-010 (lista de layers vazia)

**Retorno:** Warning exibido, ADMIN verifica configuração do servidor externo

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
