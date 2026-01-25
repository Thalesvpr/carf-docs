---
id: UC-P3-004
type: UC
modules: []
status: review
created: 2026-01-24
updated: 2026-01-24
workflow: PARTE-3
---

# UC-P3-004: Operar em Campo

Fluxo operacional completo em campo: GPS, acoes no lote, formularios, assinatura, QR Code e anexos.

## Referencia

Este UC implementa passos 15-18 do [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/03-operacao-campo.md).

## Atores

- Primario: Agente de Campo
- Secundario: Titular da Unidade

## Pre-condicoes

- Comunidade selecionada (UC-P3-003 concluido)
- Mapa carregado com poligonos

## Fluxo Principal

### Orientacao e Navegacao (Passo 15)

1. App obtem posicao via GPS do dispositivo
2. Posicao exibida no mapa em tempo real
3. Agente se orienta para chegar ao local correto
4. Comunidades, quadras e lotes visiveis no mapa
5. Cores e icones indicam status de cada lote:
   - Verde: Cadastrado/Aprovado
   - Amarelo: Pendente
   - Vermelho: Rejeitado
   - Cinza: Nao visitado
6. Agente seleciona quadra de interesse
7. Agente seleciona lote especifico

### Decisao de Acao (Passo 15.5)

8. Agente decide acao adequada:
   - **Criacao:** Novo cadastro
   - **Edicao:** Atualizar dados existentes
   - **Movimentacao:** Ajustar posicao
   - **Exclusao:** Remover cadastro (com justificativa)

### Pre-Formulario (Passo 16)

9. Agente escolhe a acao (criar/editar/mover/excluir)
10. App exibe pre-formulario
11. Agente define unidade e status inicial
12. Validacoes basicas executadas

### Formulario Completo (Passo 17)

13. App exibe formulario completo multi-etapas:
    - Dados basicos da unidade
    - Endereco completo
    - Area e dimensoes
    - Geolocalizacao (GPS ou manual)
    - Captura de fotos
14. **Validacao obrigatoria dos dados do titular:**
    - Nome completo
    - CPF (validado)
    - Documentos pessoais
15. Agente preenche todos campos obrigatorios
16. App valida dados em tempo real

### Finalizacao (Passo 18)

17. Agente salva cadastro
18. **Assinatura Digital:** Titular assina digitalmente no dispositivo
19. **Leitura de QR Code:** Para protocolos de ausencia ou pendencias
20. **Anexacao de Documentos:** Fotos de documentos, comprovantes
21. **Armazenamento Local:** Dados salvos em WatermelonDB
22. **Atualizacao de Status:** Cor/icone do lote atualizado no mapa
23. Dados disponiveis para consulta local
24. **Controle de Produtividade:** Metricas registradas

## Fluxos Alternativos

- FA-001: Voice-to-text para preenchimento
- FA-002: Copiar dados de cadastro anterior
- FA-003: Modo de exclusao com justificativa

## Fluxos de Excecao

- FE-001: GPS indisponivel
- FE-002: Memoria cheia no dispositivo
- FE-003: Bateria baixa (salvar e pausar)
- FE-004: Validacao de CPF falha

## Pos-condicoes

- Cadastro realizado em campo
- Dados armazenados localmente
- Status do lote atualizado no mapa
- Assinatura digital coletada
- Metricas de produtividade registradas
- Dados prontos para sincronizacao (UC-005)

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| RN-01 | App funciona completamente OFFLINE |
| RN-02 | Dados do titular sao OBRIGATORIOS |
| RN-03 | Assinatura digital e OBRIGATORIA |
| RN-04 | Exclusao requer justificativa |
| RN-05 | CPF deve ser valido |
