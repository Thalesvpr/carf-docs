---
modules: [GEOWEB, REURBCAD]
epic: other
---

# RF-190: Detecção de Conflitos

O sistema implementa mecanismo robusto de detecção de conflitos que identifica situações onde mesmo registro foi editado simultaneamente no servidor central (por outro usuário via web ou mobile) e localmente no dispositivo offline, cenário comum em projetos colaborativos com múltiplas equipes trabalhando concorrentemente. A detecção utiliza comparação de timestamps updated_at mantidos tanto no registro local quanto no servidor, onde conflito é identificado quando timestamp do servidor é posterior ao timestamp da última sincronização do dispositivo mas o registro também possui modificações locais não sincronizadas, indicando que ambas as versões divergiram após sincronização inicial. Ao detectar conflito durante sincronização, o sistema não sobrescreve automaticamente nenhuma das versões para prevenir perda de dados, mas sim marca o registro como em conflito e interrompe sincronização daquele item específico, permitindo que outros registros sem conflito sejam processados normalmente. O sistema apresenta interface dedicada de resolução de conflitos que exibe claramente ao usuário ambas as versões divergentes lado a lado, destacando campos que diferem entre elas e fornecendo contexto como quem editou cada versão e quando, capacitando usuário a tomar decisão informada sobre qual versão deve prevalecer ou se mesclagem de ambas é apropriada.

---

**Última atualização:** 2025-12-30
