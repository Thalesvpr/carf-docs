---
modules: [GEOWEB, REURBCAD]
epic: compatibility
---

# UC-004-FE-002: Memória Cheia

Fluxo de exceção do UC-004 Coletar Dados Campo Mobile ocorrendo no passo 9 (tirar fotos) quando app detecta espaço de armazenamento insuficiente no dispositivo impedindo salvar novas fotos, onde verificação executa periodicamente via react-native-fs checando DeviceInfo.getFreeDiskStorage() comparando com threshold mínimo configurado (tipicamente 100MB), ao tentar capturar foto sistema operacional pode retornar erro de storage full ou app pre-emptively detecta antes de abrir câmera, exibe modal de alerta com ícone vermelho título "Memória Cheia" mensagem "Espaço insuficiente para salvar fotos. Libere X MB para continuar" mostrando quantidade necessária, e oferece ações: Sincronizar Pendências disparando processo UC-005 que envia unidades pendentes para servidor e deleta dados locais após confirmação liberando storage significativo especialmente fotos que ocupam mais espaço, Gerenciar Fotos abrindo tela listando todas fotos de todas unidades locais ordenadas por tamanho permitindo FIELD_AGENT selecionar e deletar fotos grandes desnecessárias ou duplicadas, Liberar Cache limpando cache de tiles de mapa layers WMS temporários e outros arquivos temporários recuperando espaço sem perder dados de unidades, ou Cancelar impedindo tirar mais fotos mas permitindo salvar unidade sem fotos adicionais. App exibe warning persistente no header mostrando ícone de storage com percentual de uso quando >80% alertando preventivamente antes de atingir limite crítico.

**Ponto de Desvio:** Passo 9 do UC-004 (ao tentar tirar foto)

**Verificação de Storage:**

App importa getFreeDiskStorage de pacote react-native-device-info, define função async checkStorage executando await getFreeDiskStorage() retornando freeBytes em bytes, converte para megabytes calculando freeMB igual freeBytes dividido por mil e vinte e quatro vezes mil e vinte e quatro, verifica condição if freeMB menor cem chamando showStorageAlert passando freeMB exibindo modal de alerta e retornando false impedindo tirar foto, caso contrário retorna true permitindo prosseguir com captura verificando preventivamente espaço disponível antes de operação que consome storage.

**Modal de Alerta:**

Modal exibe ícone vermelho círculo com título "Memória Cheia" seguido por linha "Espaço insuficiente: X MB livres" interpolando valor real, linha "Necessário: 100 MB mínimo" mostrando threshold configurado, seção "Ações disponíveis:" com três bullet points sendo Sincronizar N unidades pendentes estimando liberação aproximada em MB calculando tamanho médio de unidade com fotos, Gerenciar M fotos locais abrindo listagem ordenada por tamanho, e Limpar cache de mapas estimando espaço recuperável de tiles WMS temporários, finalizando com quatro botões Sincronizar disparando UC-005, Gerenciar Fotos abrindo tela seleção, Limpar Cache deletando temporários, e Cancelar impedindo captura adicional.

**Liberação de Espaço:**

Após sincronização bem-sucedida app define função async deleteLocalData recebendo array syncedUnitIds executando sequencialmente await db.photos.where com unit_id aplicando anyOf com syncedUnitIds chamando delete() removendo todas fotos das unidades sincronizadas, await db.units_local.where com id aplicando anyOf com syncedUnitIds chamando delete() removendo registros de unidades locais já persistidas no servidor, executa await calculateFreedSpace() recalculando espaço disponível armazenando em freed, exibe toast interpolado "X MB liberados" informando quantidade recuperada permitindo FIELD_AGENT continuar coleta com storage limpo.

**Retorno:** Após liberar espaço, FIELD_AGENT pode continuar tirando fotos

---

**Última atualização:** 2025-12-30
