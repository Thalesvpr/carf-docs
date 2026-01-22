---
type: leaf
title: "Overview da Arquitetura"
status: review
updated: 2026-01-21
---

# Overview da Arquitetura

Biblioteca de componentes React baseada em shadcn/ui e Tailwind CSS. Dois tipos de componentes: (1) Genericos - customizacoes shadcn/ui (Button, Dialog, Table, Select) com tema CARF, e (2) Dominio - especificos REURB (UnitCard, HolderCard, CommunityCard, StatusBadge) que recebem dados via props. Dependencias: @radix-ui como peer para primitivos acessiveis, class-variance-authority para variantes, clsx+tailwind-merge para cn(). NAO depende de @carf/geoapi-client - domain components sao stateless. Stack: React 18.2, TypeScript 5.3, Tailwind 3.4, Radix UI, React Hook Form, Zod. Principios: WCAG 2.1 AA, mobile-first, tree-shakeable, 100% TypeScript.
