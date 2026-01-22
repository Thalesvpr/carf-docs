---
title: "Theming"
status: review
updated: 2026-01-21
---

# Theming

Sistema de temas via CSS variables HSL (--primary: 121 37% 27%). Light/dark mode via classe 'dark' no html. ThemeProvider com useTheme() retorna theme, setTheme e resolvedTheme, persiste no localStorage. Paleta semantica: --background, --foreground, --primary, --secondary, --muted, --accent, --destructive. Cores CARF fixas: --carf-primary (#2C5F2D), --carf-secondary (#97BC62), --carf-accent (#E63946). Status: --success, --warning, --error, --info. Customizacao via sobrescrita de variables em globals.css ou classes contextuais (.theme-admin). Contraste WCAG AA garantido. Respeita prefers-reduced-motion e prefers-contrast.
