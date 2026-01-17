---
modules: [GEOWEB]
epic: compatibility
---

# UC-010-FE-004: Erro ao Renderizar (Frontend)

Fluxo de exceção do UC-010 Configurar Camadas WMS ocorrendo no passo 17.2 quando frontend GEOWEB tenta adicionar camada ao mapa usando MapLibre GL JS addLayer mas operação falha lançando exception tipicamente causada por source URL malformada gerando requests inválidos ao servidor WMS, CORS blocking se proxy não habilitado e servidor não permite cross-origin, formato de resposta incompatível (servidor retorna image/tiff mas navegador esperava image/png), SRID não suportado por MapLibre causando erro de transformação de coordenadas, ou servidor WMS retornando HTTP 500 errors consistentemente para tiles específicos indicando problema com dados subjacentes ou configuração do GeoServer, MapLibre captura erro em event listener map.on('error') recebendo objeto com sourceId e message descrevendo falha, frontend loga erro completo no console incluindo stack trace para debug by desenvolvedores, exibe toast amarelo warning no canto superior direito da tela com ícone de alerta mensagem "Erro ao carregar camada WMS '{layer_name}'. Verifique configuração" não bloqueando interface mas alertando usuário sobre problema, adiciona badge vermelho ERROR ao item da camada no layer control lateral do mapa marcando visualmente status de falha, camada permanece listada em controle mas desabilitada impedindo toggle on/off até problema resolvido, inclui botão Detalhes do Erro no layer control que ao clicar exibe modal com mensagem de erro completa transcrita de MapLibre e sugestões de resolução como "Verifique se servidor WMS está online", "Confirme que formato suportado (PNG/JPEG)", "Habilite proxy se houver erro CORS", "Contate administrador para revisar configuração", ADMIN pode editar camada acessando menu Configurações → Camadas de Mapa clicando ícone editar no registro problemático ajustando parâmetros como layer_name format version url ou habilitando proxy tentando resolver problema, pode também deletar camada removendo configuração inválida do sistema via botão deletar confirmando ação, sistema registra erro em logs de aplicação incluindo tenant_id geoservice_id error_message timestamp permitindo equipe técnica monitorar problemas recorrentes e proativamente contatar ADMIN orientando sobre correção ou investigar issues sistêmicos como incompatibilidade com versões específicas de servidores WMS externos.

**Ponto de Desvio:** Passo 17.2 do UC-010 (MapLibre addLayer falha)

**Retorno:** Camada marcada como erro, ADMIN pode editar configuração ou remover

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
