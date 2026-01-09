---
modules: [GEOWEB, REURBCAD]
epic: usability
---

# UC-001-FE-001: Validação Falha

Fluxo de exceção do UC-001 Cadastrar Unidade Habitacional ocorrendo no passo 9 (validação de dados) quando sistema detecta erro de validação impedindo salvamento da unidade, onde validações executadas incluem campos obrigatórios preenchidos (comunidade selecionada endereço logradouro não-vazio tipo de unidade selecionado), geometria válida se fornecida (polígono fechado sem auto-interseções mínimo 3 vértices área ≥10m²), CPF titular válido se informado (11 dígitos dígitos verificadores corretos não-sequência repetida), código único dentro da comunidade verificado via query SELECT COUNT WHERE CommunityId = X AND Code = Y retornando zero, e dependendo de configurações do tenant validações adicionais customizadas definidas em CustomValidationRules JSON. Sistema ao detectar qualquer falha de validação interrompe processo de salvamento sem persistir dados parciais, constrói objeto de erro estruturado agrupando mensagens por campo afetado usando chaves i18n para internacionalização (pt-BR en-US es-ES), retorna resposta HTTP 400 Bad Request com corpo JSON contendo array de erros no formato `{"field": "address.street", "message": "Logradouro é obrigatório", "code": "REQUIRED_FIELD"}`, e frontend processa response exibindo mensagens de erro visualmente ao lado de cada campo inválido com ícone vermelho de alerta e texto explicativo, destacando campos com borda vermelha, e scrollando automaticamente viewport para primeiro campo com erro garantindo visibilidade. Usuário lê mensagens de erro compreendendo o que precisa corrigir, edita campos inválidos fornecendo dados corretos ou adicionando informações faltantes, e ao concluir correções clica novamente em botão Salvar retornando ao passo 8 do fluxo principal que dispara nova validação, repetindo ciclo até todos dados serem válidos ou usuário cancelar operação clicando Cancelar descartando dados preenchidos após confirmação via modal "Descartar alterações?". Erros comuns tratados incluem geometria com auto-interseção (exibe mapa destacando ponto de cruzamento sugerindo ajuste manual), código duplicado (exibe mensagem "Código XYZ já existe na comunidade ABC" com link para visualizar unidade conflitante), CPF inválido (exibe "CPF XXX.XXX.XXX-XX inválido" com hint sobre formato esperado), e área abaixo do mínimo (exibe "Área de Nm² está abaixo do mínimo de 10m²" sugerindo redesenhar geometria).

**Ponto de Desvio:** Passo 9 do UC-001 (validação de dados antes de salvar)

**Validações Executadas:**
- Campos obrigatórios: comunidade, endereço.logradouro, tipo
- Geometria válida: fechada, sem auto-interseção, ≥3 vértices, área ≥10m²
- CPF válido: 11 dígitos, verificadores corretos, não-sequência
- Código único: COUNT(*) WHERE CommunityId = X AND Code = Y = 0
- Validações customizadas: definidas em tenant.customValidationRules JSON

**Resposta de Erro:**
```json
{
  "errors": [
    {"field": "address.street", "message": "Logradouro é obrigatório", "code": "REQUIRED_FIELD"},
    {"field": "geometry", "message": "Geometria possui auto-interseção no vértice 5", "code": "INVALID_GEOMETRY"},
    {"field": "code", "message": "Código UH-123 já existe na comunidade", "code": "DUPLICATE_CODE"}
  ]
}
```

**Retorno:** Volta ao passo 8 do UC-001 (usuário clica Salvar) após correções

---

**Última atualização:** 2025-12-30
