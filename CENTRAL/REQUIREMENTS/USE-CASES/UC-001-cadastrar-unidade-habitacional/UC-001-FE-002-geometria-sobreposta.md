---
id: UC-001-FE-002
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-001-FE-002: Geometria Sobreposta

Fluxo de excecao do UC-001 quando geometria desenhada sobrepoe unidade existente.

## Condicao

No passo 9 do UC-001, sistema detecta sobreposicao espacial com unidades ja cadastradas.

## Fluxo

1. Sistema detecta sobreposicao com uma ou mais unidades
2. Sistema calcula percentual de area sobreposta
3. Sistema exibe modal com lista de unidades conflitantes
4. Sistema destaca geometrias no mapa (nova, existente, intersecao)
5. Usuario analisa sobreposicao visualmente
6. Usuario escolhe acao: Ajustar, Ignorar ou Cancelar

## Acoes Disponiveis

- **Ajustar Geometria**: Volta ao passo 5 para editar vertices
- **Ignorar e Salvar**: Prossegue com flag de reconhecimento (somente se <10%)
- **Cancelar**: Descarta operacao e retorna para listagem

## Retorno

- Se Ajustar: Volta ao passo 5 do UC-001
- Se Ignorar: Prossegue para passo 10 do UC-001
- Se Cancelar: Operacao abortada
