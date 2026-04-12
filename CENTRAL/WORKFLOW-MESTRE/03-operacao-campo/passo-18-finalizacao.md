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

Titular assina digitalmente no dispositivo. A tela exibe uma area de captura de assinatura com botoes Limpar e Confirmar. A assinatura e armazenada junto ao cadastro.

### 18.2 Leitura de QR Code

Para protocolos de ausencia ou pendencias. QR Code vincula documentos externos.

| Tipo | Descricao |
|------|-----------|
| Protocolo ausencia | Titular nao presente |
| Documento externo | Vinculacao de protocolo |

### 18.3 Anexacao de Documentos

Usuario anexa documentos conforme disponibilidade: fotos de documentos, comprovantes, etc.

| Documento | Obrigatorio |
|-----------|-------------|
| RG/CPF | Sim |
| Comprovante residencia | Nao |
| Escritura/Contrato | Nao |
| Outros | Nao |

### 18.4 Armazenamento Local

Dados do cadastro sao salvos no WatermelonDB local. Fotos e assinatura sao armazenadas no FileSystem local. Funciona mesmo sem conectividade.

### 18.5 Atualizacao de Status no Mapa

Status do lote atualizado imediatamente no mapa. Cor e icone refletem o novo status.

| Antes | Depois |
|-------|--------|
| Cinza (nao visitado) | Amarelo (pendente) |
| Amarelo (pendente) | Verde (cadastrado) |

### 18.6 Disponibilizacao para Consulta

Dados ficam disponiveis para consulta local. Historico de acoes registrado.

### 18.7 Controle de Produtividade

App registra metricas de produtividade:

| Metrica | Coordenador | Cadastrador |
|---------|-------------|-------------|
| Proprios cadastros | SIM | SIM |
| Metricas da equipe | SIM | NAO |
| Dashboard produtividade | SIM | NAO |

Metricas coletadas: quantidade de cadastros realizados, tempo medio por cadastro, lotes visitados por dia e taxa de conclusao.

### 18.8 Sincronizacao com Sistema Central

Quando houver conectividade, o app sincroniza bidirecionalmente com o backend GEOAPI. No PUSH, envia cadastros, fotos e assinaturas. No PULL, recebe atualizacoes como novos lotes, correcoes e status. Resolucao de conflitos segue estrategia last-write-wins, onde a versao mais recente prevalece.

## Resultado

- Cadastro completo salvo
- Assinatura coletada
- Documentos anexados
- Dados sincronizados (quando online)
- **PARTE 3 CONCLUIDA**

## Ciclo Completo

O ciclo completo segue a sequencia: Parte 1 (ortofoto entregue e processada), Parte 2 (poligonos georreferenciados e publicados), Parte 3 (cadastros realizados em campo e sincronizados). Ao concluir a Parte 3, o ciclo do workflow esta completo.
