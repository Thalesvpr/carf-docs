---
modules: [GEOWEB, REURBCAD]
epic: security
---

# UC-001: Cadastrar Unidade Habitacional

Caso de uso permitindo usuários autorizados (ANALYST com permissão para criar unidades, ADMIN com acesso total ao tenant, FIELD_AGENT usando app mobile) cadastrarem nova unidade habitacional no sistema após autenticação e verificação de permissão units.create com comunidade previamente existente, onde fluxo principal inicia com acesso à tela de cadastro exibindo formulário vazio contendo campos obrigatórios e opcionais, usuário seleciona comunidade do dropdown e preenche dados básicos incluindo código da unidade gerado automaticamente pelo sistema ou informado manualmente, endereço completo estruturado (rua número complemento CEP), tipo de unidade (Residencial Comercial Misto Institucional), e status inicial Draft, seguido por desenho de geometria espacial da unidade no mapa clicando em ferramenta de desenho de polígono marcando pontos sequencialmente no mapa e finalizando polígono com duplo-clique enquanto sistema calcula área automaticamente após fechamento da geometria, usuário preenche dados opcionais incluindo número de cômodos banheiros tipo de construção material predominante observações textuais livres, clica em botão Salvar disparando validação do sistema verificando campos obrigatórios preenchidos (comunidade endereço tipo), geometria válida fechada sem auto-interseções, CPF/CNPJ válidos se informados, código único dentro da comunidade, área mínima de 10m² respeitada, e dependendo do ator aplicando regra de negócio onde unidades criadas por FIELD_AGENT entram automaticamente em status Pending Approval ao invés de Draft, sistema salva unidade no banco com status apropriado criando registro de auditoria, exibe mensagem de sucesso contextual, e redireciona para tela de detalhes da unidade recém-criada mostrando todos campos preenchidos geometria renderizada no mapa e ações disponíveis conforme permissões. Fluxos alternativos cobertos em documentos específicos incluem desenhar geometria offline no app mobile usando GPS do dispositivo (UC-001-FA-001), importar geometria via coordenadas GeoJSON ou WKT coladas em modal (UC-001-FA-002), e copiar geometria de unidade existente próxima aplicando offset automático (UC-001-FA-003). Fluxos de exceção cobertos incluem validação falha exibindo mensagens de erro inline (UC-001-FE-001), geometria sobreposta detectada com opções de ajuste ou ignore (UC-001-FE-002), perda de conexão no mobile salvando localmente (UC-001-FE-003), e timeout de sessão com recuperação de dados (UC-001-FE-004). Pós-condições garantem unidade criada com status Draft ou Pending Approval conforme ator, registro de auditoria criado incluindo AccountId timestamp ação CREATE, unidade visível no mapa com cor correspondente ao status (cinza para Draft amarelo para Pending Approval), e unidade aparecendo em listagens filtráveis por comunidade status tipo com paginação.

**Fluxos Alternativos:**
- UC-001-FA-001: Desenhar geometria offline (mobile)
- UC-001-FA-002: Importar geometria de GPS
- UC-001-FA-003: Usar geometria de unidade existente

**Fluxos de Exceção:**
- UC-001-FE-001: Validação falha
- UC-001-FE-002: Geometria sobreposta

**Regras de Negócio:**
- RN-001: Código de unidade deve ser único dentro da comunidade (constraint banco CommunityId + Code)
- RN-002: Geometria deve ser do tipo Polygon ou MultiPolygon válido fechado sem auto-interseções
- RN-003: Área mínima 10m² calculada automaticamente após desenho de geometria
- RN-004: Apenas usuários com permissão units.create podem criar unidades verificado em middleware
- RN-005: Unidades criadas por FIELD_AGENT entram automaticamente em Pending Approval requerendo aprovação posterior

**Rastreabilidade:**
- RF-049, RF-050, RF-054, RF-055, RF-056, RF-066, RF-068, RF-069
- US-014, US-019, US-021

---

**Última atualização:** 2025-12-30
