---
modules: [GEOWEB, REURBCAD]
epic: usability
---

# UC-004-FE-001: GPS Não Disponível

Fluxo de exceção do UC-004 Coletar Dados Campo Mobile ocorrendo no passo 6 (captura GPS automática) quando app detecta que GPS está desabilitado nas configurações do dispositivo ou permissão de localização foi negada impedindo captura automática de coordenadas, onde verificação utiliza react-native-permissions checando PERMISSIONS.IOS.LOCATION_WHEN_IN_USE ou PERMISSIONS.ANDROID.ACCESS_FINE_LOCATION retornando status DENIED ou BLOCKED, app exibe modal de alerta com ícone amarelo warning título "GPS Necessário" mensagem "Precisão da localização depende do GPS. Habilitar?" e botões Habilitar GPS abrindo configurações do sistema via Linking.openSettings() permitindo usuário ativar GPS e retornar ao app que re-verifica permissão, Continuar Sem GPS permitindo prosseguir mas marcando unidade com flag low_accuracy_warning=true e desabilitando opção Caminhar Perímetro mantendo apenas desenho manual no mapa exigindo FIELD_AGENT marcar vértices manualmente com precisão visual, ou Cancelar abortando criação da unidade retornando para lista. Se continuar sem GPS app salva localização aproximada baseada em último ponto GPS conhecido (pode estar desatualizado) ou centro da tela do mapa atual se nenhum GPS available, adiciona observação automática "Cadastrado sem GPS - verificar localização" para revisão posterior, e exibe badge laranja "Baixa Precisão" permanente no card da unidade em listagens locais.

**Ponto de Desvio:** Passo 6 do UC-004 (captura GPS automática falha)

**Verificação de Permissão:**
```typescript
import { check, PERMISSIONS, request, openSettings } from 'react-native-permissions';

const checkGPS = async () => {
  const result = await check(
    Platform.OS === 'ios'
      ? PERMISSIONS.IOS.LOCATION_WHEN_IN_USE
      : PERMISSIONS.ANDROID.ACCESS_FINE_LOCATION
  );

  if (result === 'denied') {
    const requestResult = await request(permission);
    return requestResult === 'granted';
  }

  return result === 'granted';
};
```

**Modal de Alerta:**
```
⚠️ GPS Necessário

A precisão da localização depende do GPS ativado.

Sem GPS:
- Localização aproximada (baixa precisão)
- Desenho manual obrigatório
- Marcado para revisão

[Habilitar GPS] [Continuar Sem GPS] [Cancelar]
```

**Retorno:** Se habilitar GPS, retorna ao passo 6; se continuar sem, prossegue com limitações

---

**Última atualização:** 2025-12-30
