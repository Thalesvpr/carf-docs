---
modules: [GEOWEB, REURBCAD]
epic: usability
---

# UC-004-FE-001: GPS Não Disponível

Fluxo de exceção do UC-004 Coletar Dados Campo Mobile ocorrendo no passo 6 (captura GPS automática) quando app detecta que GPS está desabilitado nas configurações do dispositivo ou permissão de localização foi negada impedindo captura automática de coordenadas, onde verificação utiliza react-native-permissions checando PERMISSIONS.IOS.LOCATION_WHEN_IN_USE ou PERMISSIONS.ANDROID.ACCESS_FINE_LOCATION retornando status DENIED ou BLOCKED, app exibe modal de alerta com ícone amarelo warning título "GPS Necessário" mensagem "Precisão da localização depende do GPS. Habilitar?" e botões Habilitar GPS abrindo configurações do sistema via Linking.openSettings() permitindo usuário ativar GPS e retornar ao app que re-verifica permissão, Continuar Sem GPS permitindo prosseguir mas marcando unidade com flag low_accuracy_warning=true e desabilitando opção Caminhar Perímetro mantendo apenas desenho manual no mapa exigindo FIELD_AGENT marcar vértices manualmente com precisão visual, ou Cancelar abortando criação da unidade retornando para lista. Se continuar sem GPS app salva localização aproximada baseada em último ponto GPS conhecido (pode estar desatualizado) ou centro da tela do mapa atual se nenhum GPS available, adiciona observação automática "Cadastrado sem GPS - verificar localização" para revisão posterior, e exibe badge laranja "Baixa Precisão" permanente no card da unidade em listagens locais.

**Ponto de Desvio:** Passo 6 do UC-004 (captura GPS automática falha)

**Verificação de Permissão:**

App importa check PERMISSIONS request e openSettings de pacote react-native-permissions, define função async checkGPS executando await check passando ternário Platform.OS igual ios interrogação PERMISSIONS.IOS.LOCATION_WHEN_IN_USE dois pontos PERMISSIONS.ANDROID.ACCESS_FINE_LOCATION armazenando em result, verifica condição if result igual denied executando await request com permission armazenando em requestResult retornando requestResult igual granted se usuário concedeu, caso contrário retorna result igual granted verificando se permissão já estava concedida previamente permitindo app acessar GPS nativo do dispositivo.

**Modal de Alerta:**

Modal exibe ícone warning amarelo com título "GPS Necessário" seguido por parágrafo "A precisão da localização depende do GPS ativado." com seção destacada "Sem GPS:" listando três limitações sendo Localização aproximada com baixa precisão baseada em último ponto conhecido, Desenho manual obrigatório desabilitando opção Caminhar Perímetro, e Marcado para revisão adicionando flag low_accuracy_warning true, finalizando com três botões Habilitar GPS chamando Linking.openSettings(), Continuar Sem GPS prosseguindo com limitações, e Cancelar abortando criação.

**Retorno:** Se habilitar GPS, retorna ao passo 6; se continuar sem, prossegue com limitações

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
