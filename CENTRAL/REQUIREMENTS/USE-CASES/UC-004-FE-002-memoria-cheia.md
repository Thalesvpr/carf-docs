---
modules: [GEOWEB, REURBCAD]
epic: compatibility
---

# UC-004-FE-002: Memória Cheia

Fluxo de exceção do UC-004 Coletar Dados Campo Mobile ocorrendo no passo 9 (tirar fotos) quando app detecta espaço de armazenamento insuficiente no dispositivo impedindo salvar novas fotos, onde verificação executa periodicamente via react-native-fs checando DeviceInfo.getFreeDiskStorage() comparando com threshold mínimo configurado (tipicamente 100MB), ao tentar capturar foto sistema operacional pode retornar erro de storage full ou app pre-emptively detecta antes de abrir câmera, exibe modal de alerta com ícone vermelho título "Memória Cheia" mensagem "Espaço insuficiente para salvar fotos. Libere X MB para continuar" mostrando quantidade necessária, e oferece ações: Sincronizar Pendências disparando processo UC-005 que envia unidades pendentes para servidor e deleta dados locais após confirmação liberando storage significativo especialmente fotos que ocupam mais espaço, Gerenciar Fotos abrindo tela listando todas fotos de todas unidades locais ordenadas por tamanho permitindo FIELD_AGENT selecionar e deletar fotos grandes desnecessárias ou duplicadas, Liberar Cache limpando cache de tiles de mapa layers WMS temporários e outros arquivos temporários recuperando espaço sem perder dados de unidades, ou Cancelar impedindo tirar mais fotos mas permitindo salvar unidade sem fotos adicionais. App exibe warning persistente no header mostrando ícone de storage com percentual de uso quando >80% alertando preventivamente antes de atingir limite crítico.

**Ponto de Desvio:** Passo 9 do UC-004 (ao tentar tirar foto)

**Verificação de Storage:**
```typescript
import { getFreeDiskStorage } from 'react-native-device-info';

const checkStorage = async () => {
  const freeBytes = await getFreeDiskStorage();
  const freeMB = freeBytes / (1024 * 1024);

  if (freeMB < 100) {
    showStorageAlert(freeMB);
    return false;
  }
  return true;
};
```

**Modal de Alerta:**
```
🔴 Memória Cheia

Espaço insuficiente: 45 MB livres
Necessário: 100 MB mínimo

Ações disponíveis:
• Sincronizar 8 unidades pendentes (libera ~250 MB)
• Gerenciar 142 fotos locais (ver maiores)
• Limpar cache de mapas (libera ~80 MB)

[Sincronizar] [Gerenciar Fotos] [Limpar Cache] [Cancelar]
```

**Liberação de Espaço:**
```typescript
// Após sincronização bem-sucedida
const deleteLocalData = async (syncedUnitIds) => {
  // Deletar fotos sincronizadas
  await db.photos.where('unit_id').anyOf(syncedUnitIds).delete();
  // Deletar unidades locais
  await db.units_local.where('id').anyOf(syncedUnitIds).delete();
  // Recalcular storage
  const freed = await calculateFreedSpace();
  showToast(`${freed} MB liberados`);
};
```

**Retorno:** Após liberar espaço, FIELD_AGENT pode continuar tirando fotos

---

**Última atualização:** 2025-12-30
