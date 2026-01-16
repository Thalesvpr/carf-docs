# @carf/geoapi-client

SDK HTTP type-safe para comunicação com o backend GEOAPI, abstraindo complexidades de autenticação, retry e cache para os frontends consumidores.

## Conteúdo

Endpoints tipados cobrem todas as operações REST do GEOAPI organizados por domínio incluindo Units para CRUD de unidades habitacionais com validação geográfica, Holders para gestão de titulares com vinculação a unidades, Communities para agregação geográfica e dados demográficos, Legitimation para workflow de aprovação conforme Lei 13.465/2017, e Reports para geração de exports em múltiplos formatos.

Autenticação automática injeta JWT token em todas as requisições obtendo token do @carf/tscore, renovando silenciosamente quando próximo da expiração e redirecionando para login quando sessão expira. Tratamento de erros tipados mapeia códigos HTTP para tipos TypeScript específicos permitindo handling granular de ValidationError, NotFoundError, ForbiddenError e ServerError.

Retry logic implementa exponential backoff para falhas transientes com configuração de máximo de tentativas e delay entre retries. Circuit breaker previne cascata de falhas abrindo circuito após threshold de erros consecutivos e fechando gradualmente após período de recuperação. Suporte offline caching armazena respostas GET em IndexedDB retornando dados cached quando dispositivo está offline e sincronizando quando conexão retorna.

## Instalação

Executar comando bun add @carf/geoapi-client @carf/tscore instalando SDK junto com dependência core, configurando .npmrc para GitHub Packages registry.

## Documentação Técnica

Documentação de implementação disponível em PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/ contendo API reference, configuração e exemplos.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
