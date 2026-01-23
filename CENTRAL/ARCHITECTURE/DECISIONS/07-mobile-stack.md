---
type: adr
status: current
updated: 2026-01-22
---

# ADR-007: React Native com Expo para Mobile

## Contexto

Aplicativo mobile deve funcionar em Android e iOS para coleta de dados em campo. Recursos nativos como GPS, camera e armazenamento local sao essenciais. Equipe tem experiencia em React. Decisao impacta velocidade de desenvolvimento e manutencao de duas plataformas.

## Decisao

Adotamos React Native com Expo como framework mobile. Expo simplifica build, deploy e acesso a APIs nativas. Compartilhamento de codigo com bibliotecas @carf/tscore e @carf/ui. expo-location para GPS, expo-camera para fotos, expo-file-system para armazenamento.

## Consequencias

Codebase unico para Android e iOS reduz esforco de desenvolvimento pela metade. Reuso de conhecimento React da equipe web. Expo Go acelera ciclo de desenvolvimento. Ejection necessario para modulos nativos nao suportados. Performance inferior a nativo puro em operacoes intensivas.

## Alternativas Rejeitadas

Flutter foi descartado por linguagem Dart diferente do stack e impossibilidade de compartilhar codigo com web. Nativo puro foi rejeitado por dobrar esforco de desenvolvimento e manutencao. PWA foi descartada por limitacoes de acesso offline e recursos nativos em iOS.
