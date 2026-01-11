---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: "category"
---

# US-NNN-nome-story

Como [persona específica role ADMIN MANAGER ANALYST FISCAL FIELD_AGENT CITIZEN] quero [ação funcionalidade específica detalhada clara unambiguous] para que [benefício objetivo valor agregado problema resolvido impacto esperado mensurável observable] evitando ambiguidades sendo específico testável verificável exemplo concreto Como Técnico de Campo quero capturar coordenadas GPS automaticamente ao cadastrar unidade para que economize tempo evite erros digitação manual garantindo precisão localização geográfica facilitando análise spatial posterior relatórios mapas heatmaps density clustering identificando padrões comunidades áreas prioritárias intervenção políticas públicas direcionadas efetivas eficientes ROI mensurável impacto social regularização fundiária moradia digna direitos cidadania inclusão.

## Critérios de Aceitação

### Cenário 1: Captura GPS bem-sucedida

**Dado** técnico está em campo com dispositivo mobile GPS habilitado sinal disponível precisão < 10 metros
**Quando** abre formulário cadastro unidade toca botão "Capturar Localização"
**Então** app solicita permissão localização se não concedida exibe dialog explicando necessidade usuário concede app captura coordenadas latitude longitude exibe mapa marcador posição confirma precisão metros badge verde "Precisão: 5m" preenche automaticamente campos latitude longitude readonly usuário pode editar manual se necessário override GPS impreciso campo aberto sem edificações árvores bloqueando sinal, sistema persiste coordenadas SRID 4326 WGS84 formato decimal degrees conversão automática DMS Degrees Minutes Seconds se necessário validação range latitude -90 +90 longitude -180 +180 erro fora bounds.

### Cenário 2: GPS indisponível offline

**Dado** técnico está offline sem conectividade ou GPS desabilitado configurações device
**Quando** tenta capturar localização
**Então** app exibe mensagem "GPS indisponível, habilite nas configurações ou aguarde sinal" botão "Configurações" deeplink abrindo settings app atalho usuário habilitar retornar app automaticamente fallback entrada manual latitude longitude campos habilitados usuário digita coordenadas obtidas outro device GPS handheld externo Garmin Trimble professiona precisão centimétrica GNSS RTK Real-Time Kinematic correção diferencial base station.

### Cenário 3: Baixa precisão GPS

**Dado** sinal GPS fraco precisão > 10 metros threshold configurável
**Quando** captura coordenadas
**Então** app exibe warning badge amarelo "Precisão baixa: 25m" usuário decide aceitar aguardar melhora sinal movendo posição aberta céu visível satélites 8+ HDOP Horizontal Dilution of Precision < 2 good geometry constellation ideal atualizando real-time progressbar animação feedback visual aguardando melhora timeout 30s após exibe option aceitar baixa precisão ou cancelar manual entry.

## Notas Técnicas

Implementação usando React Native Geolocation API permissões Android LOCATION_PERMISSION iOS NSLocationWhenInUseUsageDescription Info.plist watchPosition continuous updates accuracy highAccuracy distanceFilter 10 meters callback success error handling timeout maximumAge caching preventing stale positions offline storage WatermelonDB SQLite sync pending uploads background geofencing optional triggering notifications usuário próximo unit cadastrada reminder follow-up photos documentation complete workflow mobile-first UX optimized thumb reachability bottom navigation floating action button FAB material design iOS Human Interface Guidelines platform-specific adaptations respecting conventions users familiar comfortable reducing cognitive load learning curve onboarding tutorials tooltips progressive disclosure advanced features expert users shortcuts gestures swipe actions contextual menus accessibility VoiceOver TalkBack screen readers semantic labels ARIA WCAG 2.1 AA compliance inclusive design universal usability disabilities visual motor cognitive diverse abilities needs.

## Rastreabilidade

- **Requisitos Funcionais**: RF-012-captura-gps-automatica
- **Use Cases**: UC-001-cadastrar-unidade-habitacional
- **Technical Specs**: REURBCAD/docs/gps-integration.md

---

**Última atualização:** YYYY-MM-DD
