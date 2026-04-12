---
id: UC-007-FE-002
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-007-FE-002: Geometrias Invalidas

Fluxo de excecao do UC-007 quando algumas geometrias sao invalidas.

## Condicao

Durante processamento do UC-007, sistema detecta geometrias com problemas topologicos.

## Fluxo

1. Sistema processa cada registro
2. Sistema valida geometria antes de serializar
3. Sistema detecta geometria invalida
4. Sistema registra warning no log
5. Sistema pula registro invalido
6. Sistema continua processando demais registros
7. Sistema inclui aviso na notificacao final

## Problemas Detectados

- Auto-intersecoes (poligono cruzando a si proprio)
- Aneis nao fechados
- Geometrias degeneradas (area zero)
- Coordenadas corrompidas

## Retorno

Registros invalidos ignorados. Exportacao continua com unidades validas. Warning na notificacao.

## Pos-condicoes

- Arquivo contem apenas geometrias validas
- Usuario informado sobre registros ignorados
- Log disponivel para identificar unidades problematicas
