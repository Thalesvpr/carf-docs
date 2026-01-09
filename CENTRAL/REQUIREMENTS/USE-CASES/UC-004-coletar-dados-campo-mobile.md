---
modules: [GEOWEB, REURBCAD]
epic: security
---

# UC-004: Coletar Dados em Campo (Mobile)

Caso de uso permitindo FIELD_AGENT agente de campo usar app mobile REURBCAD React Native para cadastrar unidades habitacionais offline diretamente no local durante jornada de levantamento em campo após instalação do app em dispositivo Android ou iOS, autenticação prévia, sincronização inicial de dados da comunidade alvo baixando boundaries camadas WMS referências necessárias, e habilitação de GPS no dispositivo para captura precisa de localização. Fluxo principal inicia com FIELD_AGENT chegando fisicamente na localização da unidade habitacional a cadastrar, app detecta automaticamente modo offline verificando conectividade via NetInfo listener mostrando badge laranja Offline no header indicando operação local sem comunicação com servidor, FIELD_AGENT navega até posição exata usando mapa offline previamente cached com tiles do OpenStreetMap ou MapBox visualizando unidades já cadastradas como polígonos coloridos e localização atual como pin azul pulsante, clica em botão flutuante Nova Unidade abrindo formulário de cadastro otimizado para mobile com campos grandes touch-friendly e teclado contextual adequado para cada tipo de dado (numérico para número endereço, alfanumérico para logradouro, email keyboard para email). App captura localização GPS atual automaticamente em background usando react-native-geolocation-service armazenando latitude longitude accuracy altitude timestamp como ponto de referência inicial da unidade mostrando precisão em metros com ícone verde <5m amarelo 5-10m vermelho >10m alertando se precisão inadequada, FIELD_AGENT preenche dados básicos incluindo endereço com autocomplete de logradouro usando cache local de ruas da comunidade baixadas previamente acelerando digitação em campo, seletor de tipo de unidade (Residencial Comercial Misto Institucional Vago) com ícones visuais facilitando identificação rápida, campo numérico número de moradores com stepper + e - para ajuste fácil sem teclado, e observações com voice-to-text opcional quando FIELD_AGENT prefere ditar ao invés de digitar. FIELD_AGENT desenha geometria espacial da unidade usando uma de duas opções disponíveis: Opção 1 Caminhar Perímetro ativa GPS tracking contínuo onde agente fisicamente caminha ao redor do perímetro da propriedade enquanto app coleta pontos GPS a cada 3-5 metros ou ao pressionar botão Marcar Ponto manualmente formando polígono automaticamente e exibindo trilha em tempo real no mapa offline, ou Opção 2 Desenhar Manual permite marcar vértices diretamente no mapa touchscreen com zoom facilitando precisão em áreas densas ou quando caminhar é impraticável. FIELD_AGENT tira fotos documentais clicando botão Tirar Foto que abre câmera nativa do dispositivo via react-native-camera, captura múltiplas fotos (fachada frontal lateral fundos interior cômodos específicos), app salva cada foto localmente em storage do app com compressão automática para economizar espaço (JPEG quality 80% max 1920x1080), adiciona geotag EXIF automático com lat/lng se GPS disponível permitindo posterior mapeamento visual de onde foto foi tirada, permite adicionar descrição textual ou por voz para cada foto (Fachada frontal, Sala de estar, Quintal), e exibe galeria de thumbnails com contador "5/20 fotos" respeitando limite de 20 fotos por unidade configurado para evitar storage explosion em dispositivos com muitas unidades pendentes. FIELD_AGENT cadastra titular morador diretamente no local clicando Adicionar Morador abrindo formulário inline com nome completo, CPF com validação em tempo real mesmo offline usando algoritmo local, telefone celular para contato futuro, e opção Tirar Foto do Documento capturando imagem de RG ou carteira CNH armazenando como attachment do titular para verificação posterior no escritório durante aprovação. FIELD_AGENT ao concluir clica botão Salvar disparando validações locais verificando campos obrigatórios preenchidos geometria tem mínimo 3 pontos formando polígono válido CPF titular válido se informado, app salva todos dados em banco SQLite local usando WatermelonDB ORM criando registros nas tabelas units_local holders_local unit_holders_local photos_local com UUID gerado localmente (uuid v4) servindo como identificador temporário até sincronização com servidor que retornará GUID definitivo, marca status automaticamente como Pending Approval conforme regra RN-001 que dados de FIELD_AGENT requerem revisão antes de aprovar, adiciona flag needs_sync=true indicando pendência de sincronização, exibe toast de sucesso "Unidade salva localmente" com badge laranja Pendente Sincronização, incrementa contador de pendências no tab inferior mostrando "12 pendentes" alertando visualmente quantidade acumulada, e permite FIELD_AGENT continuar imediatamente para próxima unidade sem delay mantendo fluxo rápido de trabalho em campo. Fluxos alternativos incluem sincronizar imediatamente se conexão disponível (UC-004-FA-001), usar voice-to-text para preencher campos falando (UC-004-FA-002), e copiar dados da unidade anterior quando propriedades adjacentes têm características similares (UC-004-FA-003). Fluxos de exceção cobrem GPS não disponível permitindo continuar com marcação manual (UC-004-FE-001), memória cheia bloqueando novas fotos até sincronizar ou liberar espaço (UC-004-FE-002), e bateria baixa ativando modo economia (UC-004-FE-003).

**Fluxos Alternativos:**
- [UC-004-FA-001: Sincronizar imediatamente](UC-004-FA-001-sincronizar-imediato.md)
- [UC-004-FA-002: Voice-to-text](UC-004-FA-002-voice-to-text.md)
- [UC-004-FA-003: Copiar unidade anterior](UC-004-FA-003-copiar-anterior.md)

**Fluxos de Exceção:**
- [UC-004-FE-001: GPS não disponível](UC-004-FE-001-gps-indisponivel.md)
- [UC-004-FE-002: Memória cheia](UC-004-FE-002-memoria-cheia.md)
- [UC-004-FE-003: Bateria baixa](UC-004-FE-003-bateria-baixa.md)

**Regras de Negócio:**
- RN-001: Dados coletados offline por FIELD_AGENT entram automaticamente em Pending Approval requerendo revisão ANALYST/MANAGER
- RN-002: Fotos devem ter geotag EXIF (lat lng timestamp) quando GPS disponível facilitando mapeamento visual
- RN-003: Limite 20 fotos por unidade no mobile para evitar storage overflow (web sem limite)
- RN-004: Geometria mínima 3 pontos válidos formando triângulo (área não-degenerada)
- RN-005: Dados locais não sincronizados devem ser enviados em até 7 dias (alerta automático após 5 dias)

**Rastreabilidade:**
- RF-049, RF-063, RF-064, RF-122, RF-123, RF-182, RF-184, RF-186
- US-040, US-042, US-044

---

**Última atualização:** 2025-12-30
