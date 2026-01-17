---
modules: [GEOWEB, REURBCAD]
epic: compatibility
---

# RF-184: Criar Unidade Offline

O sistema permite criação completa de unidades territoriais no aplicativo mobile sem necessidade de conexão com internet, através de formulário totalmente funcional offline que captura todos os atributos obrigatórios incluindo identificação, tipo de ocupação, geometria espacial desenhada no mapa, e vinculação com titulares. Durante criação offline, o sistema gera automaticamente UUID (Universally Unique Identifier) localmente no dispositivo para identificar univocamente a unidade, garantindo que mesmo múltiplos dispositivos operando simultaneamente offline não gerem conflitos de identificação ao sincronizar posteriormente com servidor central. A unidade criada é marcada automaticamente com flag de "pendente sincronização" que indica visualmente ao usuário através de ícone distintivo que aquele registro foi criado localmente e ainda não foi persistido no banco de dados central, auxiliando no controle de quais dados já foram efetivamente sincronizados. Todas as validações de negócio aplicáveis são executadas localmente durante criação offline, incluindo verificação de campos obrigatórios, validação de formatos e consistência de dados, garantindo que apenas informações válidas sejam aceitas mesmo sem conectividade com servidor que normalmente executaria essas validações.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
