---
modules: [GEOAPI, REURBCAD]
epic: compatibility
---

# RF-189: Delta Sync (Sincronização Incremental)

O sistema implementa sincronização incremental eficiente que transmite apenas dados alterados desde última sincronização bem-sucedida, em contraste com sincronização completa que transferiria todos os dados a cada operação, reduzindo drasticamente tempo de sincronização e consumo de banda especialmente relevante em contextos de conectividade limitada. A implementação mantém timestamps de última sincronização persistidos localmente no dispositivo e utiliza endpoint especializado /api/sync/pull que aceita parâmetro lastPulledAt permitindo ao servidor retornar apenas registros criados ou modificados após aquele timestamp, minimizando payload da resposta. Na direção oposta (push), o aplicativo envia ao servidor apenas dados criados ou editados localmente desde última sincronização, identificados através de flags de pendência e timestamps de modificação mantidos no banco SQLite local, evitando retransmissão de dados já sincronizados previamente. Este padrão de sincronização incremental (delta sync) é fundamental para viabilizar uso do sistema em áreas com conectividade precária onde sincronizações completas seriam impraticáveis devido a tempo excessivo ou custos proibitivos de dados móveis, permitindo que projetos de regularização fundiária sejam executados eficientemente mesmo em contextos tecnologicamente desafiadores típicos de comunidades informais periféricas ou rurais.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
