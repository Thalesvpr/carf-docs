---
type: workflow
status: approved
updated: 2026-01-25
category: regras
---

# Regras de Operacao em Campo

Regras que definem as funcionalidades obrigatorias do fluxo de campo.

## Regras

| Regra | Descricao |
|-------|-----------|
| CAMPO-01 | Fluxo de campo INCLUI modo online/offline |
| CAMPO-02 | Fluxo de campo INCLUI GPS para orientacao |
| CAMPO-03 | Fluxo de campo INCLUI acoes no lote (criar/editar/mover/excluir) |
| CAMPO-04 | Fluxo de campo INCLUI formularios de cadastro |
| CAMPO-05 | Fluxo de campo INCLUI assinatura digital |
| CAMPO-06 | Fluxo de campo INCLUI leitura de QR Code |
| CAMPO-07 | Fluxo de campo INCLUI anexacao de documentos |
| CAMPO-08 | Fluxo de campo INCLUI armazenamento local |
| CAMPO-09 | Fluxo de campo INCLUI sincronizacao com central |

## Detalhamento

### CAMPO-01: Online/Offline

O app deve funcionar em ambos os modos:
- Online: Dados em tempo real
- Offline: Dados locais (WatermelonDB)
- Transicao transparente entre modos

### CAMPO-02: GPS

Orientacao geografica obrigatoria:
- Posicao exibida no mapa
- Navegacao ate o lote
- Registro de coordenadas no cadastro

### CAMPO-03: Acoes no Lote

Quatro acoes disponiveis:
- **Criar**: Novo cadastro
- **Editar**: Atualizar existente
- **Mover**: Ajustar geometria
- **Excluir**: Remover (com justificativa)

### CAMPO-04: Formularios

Cadastro completo multi-etapas:
- Dados basicos
- Endereco
- Area e dimensoes
- Geolocalizacao
- Titular
- Fotos

### CAMPO-05: Assinatura Digital

Coleta obrigatoria de assinatura:
- Titular assina no dispositivo
- Armazenada com o cadastro
- Validade juridica

### CAMPO-06: QR Code

Leitura para vincular documentos:
- Protocolos de ausencia
- Documentos externos
- Rastreabilidade

### CAMPO-07: Anexacao

Documentos podem ser anexados:
- RG/CPF (obrigatorio)
- Comprovante residencia
- Escritura/Contrato
- Outros

### CAMPO-08: Armazenamento Local

Dados salvos no dispositivo:
- WatermelonDB para dados estruturados
- FileSystem para arquivos
- Funciona sem conexao

### CAMPO-09: Sincronizacao

Troca de dados com backend:
- PUSH: Envio de dados locais
- PULL: Recebimento de atualizacoes
- Resolucao de conflitos (last-write-wins)
