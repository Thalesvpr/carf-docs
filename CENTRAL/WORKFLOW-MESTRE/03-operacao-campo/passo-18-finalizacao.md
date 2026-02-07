---
type: workflow
status: approved
updated: 2026-02-07
part: 3
step: 18
---

# Passo 18: Finalizacao e Sincronizacao

Apos salvar o cadastro, o fluxo finaliza com assinatura, anexos e sincronizacao.

## Atores

- **Coordenador de Campo**: finaliza cadastro + ve metricas de equipe
- **Cadastrador de Campo**: finaliza cadastro

## Sub-passos

### 18.1 Assinatura Digital

- Titular assina digitalmente no dispositivo
- Assinatura armazenada com o cadastro

```
┌─────────────────────────────┐
│  ASSINATURA DIGITAL         │
├─────────────────────────────┤
│  ┌───────────────────────┐  │
│  │                       │  │
│  │    [area de          │  │
│  │     assinatura]      │  │
│  │                       │  │
│  └───────────────────────┘  │
│  [LIMPAR]     [CONFIRMAR]   │
└─────────────────────────────┘
```

### 18.2 Leitura de QR Code

- Para protocolos de ausencia ou pendencias
- QR Code vincula documentos externos

| Tipo | Descricao |
|------|-----------|
| Protocolo ausencia | Titular nao presente |
| Documento externo | Vinculacao de protocolo |

### 18.3 Anexacao de Documentos

- Usuario anexa documentos conforme disponibilidade
- Fotos de documentos, comprovantes, etc.

| Documento | Obrigatorio |
|-----------|-------------|
| RG/CPF | Sim |
| Comprovante residencia | Nao |
| Escritura/Contrato | Nao |
| Outros | Nao |

### 18.4 Armazenamento Local

- Dados salvos localmente (WatermelonDB)
- Arquivos armazenados para envio posterior
- **Funciona mesmo SEM conectividade**

```
Cadastro ──> WatermelonDB (local)
Fotos ──> FileSystem (local)
Assinatura ──> FileSystem (local)
```

### 18.5 Atualizacao de Status no Mapa

- Status do lote atualizado IMEDIATAMENTE no mapa
- Cor/icone reflete novo status

| Antes | Depois |
|-------|--------|
| ⚪ Cinza (nao visitado) | 🟡 Amarelo (pendente) |
| 🟡 Amarelo (pendente) | 🟢 Verde (cadastrado) |

### 18.6 Disponibilizacao para Consulta

- Dados ficam disponiveis para consulta local
- Historico de acoes registrado

### 18.7 Controle de Produtividade

App registra metricas de produtividade:

| Metrica | Coordenador | Cadastrador |
|---------|-------------|-------------|
| Proprios cadastros | SIM | SIM |
| Metricas da equipe | SIM | NAO |
| Dashboard produtividade | SIM | NAO |

Metricas coletadas:
- Quantidade de cadastros realizados
- Tempo medio por cadastro
- Lotes visitados por dia
- Taxa de conclusao

### 18.8 Sincronizacao com Sistema Central

Quando houver conectividade:

**PUSH (envio):**
- App envia dados para o backend
- Cadastros, fotos, assinaturas

**PULL (recebimento):**
- App recebe atualizacoes do backend
- Novos lotes, correcoes, status

**Resolucao de Conflitos:**
- Estrategia: last-write-wins
- Versao mais recente prevalece

```
App Local ←──PULL──→ Backend GEOAPI
         ←──PUSH──→
```

## Resultado

- Cadastro completo salvo
- Assinatura coletada
- Documentos anexados
- Dados sincronizados (quando online)
- **PARTE 3 CONCLUIDA**

## Ciclo Completo

```
PARTE 1: Ortofoto entregue e processada
    │
    v
PARTE 2: Poligonos georreferenciados e publicados
    │
    v
PARTE 3: Cadastros realizados em campo e sincronizados
    │
    v
   FIM DO CICLO
```
