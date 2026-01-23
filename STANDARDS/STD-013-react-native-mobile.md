---
type: standard
status: review
updated: 2026-01-22
---

# STD-013: React Native para Mobile

## Regra

Aplicativos mobile devem usar React Native 0.76+ com Expo SDK. Proibido Flutter, desenvolvimento nativo puro, Ionic ou PWA para apps principais.

## Justificativa

Code reuse 70-80% entre iOS e Android. Compartilha logica TypeScript com frontend web. Equipe ja domina React. OTA updates sem review de stores.

## Aplicacao

Projeto REURBCAD e qualquer novo app mobile. Usa WatermelonDB para offline-first com sincronizacao bidirecional.
