---
type: leaf
title: "Data Flow"
status: review
updated: 2026-01-21
---

# Data Flow

Fluxo unidirecional: Props Down, Events Up. Componentes pais passam dados via props, filhos emitem eventos via callbacks (onClick, onChange, onSubmit). State management e responsabilidade das aplicacoes consumidoras (GEOWEB/ADMIN), componentes da lib sao controlled e stateless quando possivel, mantendo apenas UI state interno (modals abertos, tabs ativas) via useState local. Dados de dominio (Units, Holders, Communities) sao sempre props controladas externamente. Para forms complexos, hooks customizados (useUnitForm) encapsulam logica de validacao via React Hook Form + Zod.
