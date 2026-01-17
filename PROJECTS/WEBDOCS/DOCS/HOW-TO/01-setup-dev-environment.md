# Setup Dev Environment - WEBDOCS

## Setup

Setup requer Node.js 18+ ou Bun 1.0+, clonar repositório `git clone https://github.com/user/carf-webdocs.git PROJECTS/WEBDOCS/SRC-CODE`, instalar dependências com `bun install`, sincronizar docs de CENTRAL com `bun run sync-docs` copiando arquivos Markdown para `src/content/docs/`, e rodar dev server com `bun run dev` abrindo `http://localhost:4321` com hot reload automático ao editar arquivos Markdown ou components, VS Code extensions recomendadas são Astro, MDX, Tailwind CSS IntelliSense, e Markdownlint.

## Passo a Passo

```bash
# 1. Clonar
git clone https://github.com/user/carf-webdocs.git PROJECTS/WEBDOCS/SRC-CODE
cd PROJECTS/WEBDOCS/SRC-CODE

# 2. Instalar
bun install

# 3. Sincronizar docs
bun run sync-docs

# 4. Rodar dev server
bun run dev  # http://localhost:4321
```

## VS Code Extensions

- Astro (astro-build.astro-vscode)
- MDX (unifiedjs.vscode-mdx)
- Tailwind CSS IntelliSense (bradlc.vscode-tailwindcss)
- Markdownlint (DavidAnson.vscode-markdownlint)

## Referências

- [Astro Installation](https://docs.astro.build/en/install/auto/)
- [Starlight Setup](https://starlight.astro.build/getting-started/)

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Muitas listas com bullets (6) antes do rodapé - considerar converter para parágrafo denso; Contém code blocks - considerar converter para prosa.
