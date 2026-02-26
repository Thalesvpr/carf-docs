---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
---

# RF-164: Calcular Perfil Topografico

## Descricao

Sistema deve fornecer ferramenta interativa para calculo de perfil topografico permitindo tracar linha arbitraria no mapa definindo secao transversal sobre a qual serao amostrados valores de elevacao do terreno. Durante tracado, sistema captura coordenadas dos vertices e ao finalizar realiza amostragem sistematica de elevacao ao longo de toda extensao, interpolando valores altimetricos a partir de pontos topograficos ou MDE. Resultado apresentado em grafico bidimensional onde eixo horizontal representa distancia acumulada e eixo vertical representa altitude, permitindo visualizar variacoes de relevo, identificar pontos de maxima e minima elevacao e calcular declividades. Fundamental para analise de viabilidade de infraestrutura linear (vias, drenagem) e identificacao de areas sujeitas a processos erosivos.

## Criterios de Aceitacao

1. Tracado de linha interativo no mapa
2. Amostragem de elevacao ao longo do trajeto
3. Grafico distancia x altitude
4. Identificacao de maximas e minimas
5. Calculo de declividades

## Rastreabilidade

- Modulos: REURBWEB
- Requisitos dependentes: RF-160, RF-163
