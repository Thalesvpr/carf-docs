---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-080: Dividir Unidade

## Descricao

Sistema deve permitir que usuarios ADMIN dividam uma unidade em multiplas unidades atraves de desenho de linha divisoria no mapa. Ferramenta de split possibilita criacao de poligonos resultantes via particao geometrica ST_Split. Usuario clica vertices definindo trajetoria de corte que intersecta poligono original. Para cada poligono resultante, sistema cria registro herdando atributos basicos mas requerendo codigos unicos. Titulares podem ser distribuidos entre novas unidades ou duplicados em todas.

## Criterios de Aceitacao

1. Desenho de linha divisoria no mapa
2. Split geometrico via ST_Split
3. Criacao de registros por poligono resultante
4. Especificacao de codigos unicos
5. Restrito a perfil ADMIN

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-049, RF-066
