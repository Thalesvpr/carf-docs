---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: portability
---

# UC-004-FA-002: Voice-to-Text

Fluxo alternativo do UC-004 Coletar Dados Campo Mobile desviando no passo 7 (preencher dados básicos) quando FIELD_AGENT prefere ditar informações ao invés de digitar acelerando coleta em campo especialmente útil quando usando luvas mãos sujas ou em movimento, onde ao lado de cada campo de texto app exibe ícone de microfone, FIELD_AGENT clica no ícone disparando reconhecimento de voz via react-native-voice usando Speech Recognition API nativa do iOS/Android, app exibe modal com onda sonora animada indicando escuta ativa e botão Parar, FIELD_AGENT fala informações de forma natural "Rua das Flores número cinquenta e três" ou "Tipo residencial quatro moradores", sistema transcreve áudio para texto em tempo real usando engine do dispositivo (offline-capable em dispositivos modernos) ou Google Speech API se online, preenche automaticamente campo correspondente com texto transcrito aplicando formatação básica (capitalização de endereço, conversão de números por extenso para dígitos), permite FIELD_AGENT revisar e editar texto se transcrição incorreta, e repete processo para múltiplos campos economizando tempo de digitação significativo.

**Ponto de Desvio:** Passo 7 do UC-004 (ao invés de digitar, dita)

**Implementação:**

App importa Voice de pacote @react-native-voice/voice, define função async startVoiceRecognition recebendo fieldName como parâmetro, executa await Voice.start passando locale pt-BR ativando reconhecimento de voz em português brasileiro usando engine nativa do dispositivo iOS Speech Recognition ou Android SpeechRecognizer, define callback Voice.onSpeechResults recebendo evento e extraindo text de e.value[0] pegando primeiro resultado transcrito com maior confiança, chama setFieldValue passando fieldName e formatText(text) aplicando formatação básica como capitalização de endereços conversão de números por extenso para dígitos preenchendo campo automaticamente com texto transcrito permitindo FIELD_AGENT revisar e editar se necessário antes de prosseguir.

**Retorno:** Campo preenchido via voz, FIELD_AGENT continua para próximo campo

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
