---
type: leaf
status: review
updated: 2026-02-21
---

# Integracao REURBCAD com Bibliotecas Compartilhadas

Documentacao de como o aplicativo mobile REURBCAD consome as bibliotecas compartilhadas @carf/tscore, @carf/geoapi-client e @carf/ui-native.

## @carf/tscore/auth

REURBCAD inicializa o KeycloakClient com adapters mobile especificos. MobileStorageAdapter usa expo-secure-store para persistir tokens de forma segura no dispositivo. MobileNavigationAdapter integra com expo-router para deep linking no callback OAuth2. O scope offline_access e solicitado no login para obter refresh token de 30 dias, permitindo uso em campo sem reconexao frequente.

## @carf/tscore/validations

Validacoes de CPF e CNPJ integram com formularios Zod no REURBCAD. O schema de cadastro de titular usa cpf.isValid() e cnpj.isValid() como refinements do Zod. Validacao ocorre localmente no dispositivo antes de sincronizar com backend, evitando rejeicoes durante sync.

## @carf/tscore/types

REURBCAD importa todas as interfaces de entidade (Unit, Holder, Community, Block, Plot, Building, Document) e enums (UnitStatus, HolderType, CommunityType, Role, TeamRole, AttendanceStatus, SyncStatus) do tscore. Tipos sao usados em todo o app para type safety end-to-end: formularios, WatermelonDB models, sync queue e renderizacao de componentes.

## @carf/geoapi-client

O GeoApiClient e instanciado com interceptors customizados para suporte offline. Quando dispositivo esta offline, requests sao enfileirados no sync queue local (WatermelonDB). Ao reconectar, o SyncManager usa api.sync.pushChanges() para enviar mudancas pendentes e api.sync.pullChanges() para receber atualizacoes do servidor. Conflitos de versao sao resolvidos com estrategia server-wins por padrao, com opcao de revisao manual pelo coordenador.

## @carf/ui-native

Componentes de UI seguem o padrao de copia local inspirado no shadcn/ui. Componentes sao copiados da biblioteca para o projeto e customizados conforme necessidade. Isso permite ajustes especificos sem afetar outros consumidores. Componentes de dominio (UnitCard, HolderCard, StatusBadge, CommunityCard, MapComponent, SignatureCanvas) integram diretamente com tipos do tscore.

## Mapa de Dependencias

| Biblioteca | Modulo | Componentes Consumidos |
|:-----------|:-------|:-----------------------|
| @carf/tscore | auth | KeycloakClient, MobileStorageAdapter, MobileNavigationAdapter |
| @carf/tscore | validations | CPF, CNPJ, Email, Phone, schemas Zod |
| @carf/tscore | types | Unit, Holder, Community, Block, Plot, enums |
| @carf/geoapi-client | CRUD | units, holders, communities |
| @carf/geoapi-client | sync | pullChanges, pushChanges, getStatus |
| @carf/geoapi-client | packages | downloadField para dados offline |
| @carf/geoapi-client | orthofotos | getOrtofoto para camada de mapa |
| @carf/ui-native (copiado) | FORM | Button, Input, Select, Checkbox, Switch, Textarea |
| @carf/ui-native (copiado) | LAYOUT | Card, Tabs, BottomSheet |
| @carf/ui-native (copiado) | FEEDBACK | Alert, Toast, Dialog, Progress, OfflineIndicator |
| @carf/ui-native (copiado) | DOMAIN | UnitCard, HolderCard, StatusBadge, CommunityCard, Map, Camera, Signature |
| @carf/ui-native (copiado) | NAVIGATION | BottomNavigation role-aware |
