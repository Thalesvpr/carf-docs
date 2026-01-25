---
type: workflow
status: approved
updated: 2026-01-25
part: 3
step: 17
---

# Passo 17: Formulario Completo de Cadastro

Agente preenche formulario completo multi-etapas com todos os dados do cadastro.

## Fluxo

1. App exibe formulario completo multi-etapas:
   - Dados basicos da unidade
   - Endereco completo
   - Area e dimensoes
   - Geolocalizacao (GPS ou manual)
   - Captura de fotos
2. **Validacao obrigatoria dos dados do titular:**
   - Nome completo
   - CPF (validado)
   - Documentos pessoais
3. Agente preenche todos campos obrigatorios
4. App valida dados em tempo real

## Etapas do Formulario

### Etapa 1: Dados Basicos

| Campo | Tipo | Obrigatorio |
|-------|------|-------------|
| Codigo do lote | Texto | Sim |
| Tipo de unidade | Selecao | Sim |
| Status de ocupacao | Selecao | Sim |

### Etapa 2: Endereco

| Campo | Tipo | Obrigatorio |
|-------|------|-------------|
| Logradouro | Texto | Sim |
| Numero | Texto | Sim |
| Complemento | Texto | Nao |
| Bairro | Texto | Sim |
| CEP | Texto | Nao |

### Etapa 3: Area e Dimensoes

| Campo | Tipo | Obrigatorio |
|-------|------|-------------|
| Area total (m²) | Numero | Sim |
| Area construida (m²) | Numero | Sim |
| Frente (m) | Numero | Nao |
| Fundo (m) | Numero | Nao |

### Etapa 4: Geolocalizacao

| Campo | Tipo | Obrigatorio |
|-------|------|-------------|
| Latitude | Numero | Sim |
| Longitude | Numero | Sim |
| Precisao GPS | Numero | Auto |

### Etapa 5: Titular

| Campo | Tipo | Obrigatorio |
|-------|------|-------------|
| Nome completo | Texto | **SIM** |
| CPF | CPF | **SIM** |
| RG | Texto | Nao |
| Data nascimento | Data | Nao |
| Telefone | Telefone | Nao |

### Etapa 6: Fotos

| Campo | Tipo | Obrigatorio |
|-------|------|-------------|
| Foto fachada | Imagem | Sim |
| Foto documento | Imagem | Sim |
| Fotos adicionais | Imagens | Nao |

## Validacoes em Tempo Real

- CPF valido (digitos verificadores)
- Campos obrigatorios preenchidos
- Formatos corretos (telefone, CEP)
- Coordenadas dentro do poligono do lote

## Resultado

- Formulario completo preenchido
- Dados validados
- Pronto para finalizacao

## Proximo Passo

Passo 18: Finalizacao e Sincronizacao
