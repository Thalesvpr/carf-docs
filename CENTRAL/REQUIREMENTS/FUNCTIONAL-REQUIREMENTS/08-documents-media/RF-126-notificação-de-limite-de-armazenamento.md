---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: compatibility
---

# RF-126: Notificação de Limite de Armazenamento

Este requisito especifica que administradores de tenant devem ser notificados proativamente quando uso de storage atinge 80% da quota configurada permitindo ação preventiva antes de limite ser atingido e uploads bloqueados, onde sistema monitora continuamente ou periodicamente percentual de uso relativo à quota. O sistema deve implementar monitoramento de uso através de job agendado ou trigger que verifica periodicamente consumo atual de cada tenant comparando com quota configurada, calculando percentual utilizado e identificando tenants que ultrapassaram threshold de alerta configurado tipicamente 80%. Quando threshold é atingido, sistema deve enviar email de alerta para administradores do tenant incluindo informações sobre uso atual quota total percentual consumido e orientações sobre como liberar espaço ou solicitar aumento de quota, garantindo que responsáveis tenham conhecimento da situação antes que se torne crítica. Além de email, o sistema deve exibir painel com métricas de storage no módulo administrativo mostrando visualmente progresso de uso através de gráfico ou barra de progresso com indicadores de alerta em amarelo quando próximo do limite e vermelho quando quota excedida. O sistema deve registrar envio de notificações para evitar spam repetitivo, enviando alertas máximo uma vez por período configurado. A funcionalidade deve ser implementada no módulo GEOAPI através de background jobs e integração com serviço de email.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
