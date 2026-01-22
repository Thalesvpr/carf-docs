---
type: leaf
status: review
updated: 2026-01-21
---

# Scripts de Validação

Scripts TypeScript completos para validação da documentação.

Arquivos relacionados:
- Regras de validação: `17-validation-rules.md`
- Integração CI: `17-validation-ci.md`

## Script Principal (validate-sources.ts)

```typescript
// scripts/validate-sources.ts
import { glob } from 'glob';
import { readFile, access } from 'fs/promises';
import matter from 'gray-matter';
import path from 'path';

interface Violation {
  ruleId: string;
  severity: 'ERROR' | 'WARNING' | 'INFO';
  file: string;
  line?: number;
  message: string;
  suggestion?: string;
}

interface ValidationResult {
  violations: Violation[];
  stats: {
    filesChecked: number;
    errors: number;
    warnings: number;
    infos: number;
  };
}

const SOURCE_PATTERN = /^(CENTRAL|PROJECTS)\/[\w\-\/]+\.md$/;
const DOCS_REPO_PATH = process.env.DOCS_REPO_PATH || '../carf-docs';

async function fileExists(filePath: string): Promise<boolean> {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function validateSources(): Promise<ValidationResult> {
  const violations: Violation[] = [];
  const files = await glob('src/content/docs/**/*.mdx', {
    ignore: ['**/index.mdx', '**/_*.mdx']
  });

  for (const file of files) {
    const content = await readFile(file, 'utf-8');
    const { data: frontmatter } = matter(content);

    // SRC001: Source Required
    if (!frontmatter.source) {
      violations.push({
        ruleId: 'SRC001',
        severity: 'ERROR',
        file,
        message: 'Campo source é obrigatório no frontmatter',
        suggestion: 'Adicione source: "CENTRAL/path/to/file.md"'
      });
      continue;
    }

    // SRC004: Source Format
    if (!SOURCE_PATTERN.test(frontmatter.source)) {
      violations.push({
        ruleId: 'SRC004',
        severity: 'ERROR',
        file,
        message: `Source "${frontmatter.source}" não segue padrão esperado`,
        suggestion: 'Formato: CENTRAL/PATH/file.md ou PROJECTS/PATH/file.md'
      });
      continue;
    }

    // SRC002: Source Exists
    const sourcePath = path.join(DOCS_REPO_PATH, frontmatter.source);
    if (!(await fileExists(sourcePath))) {
      violations.push({
        ruleId: 'SRC002',
        severity: 'ERROR',
        file,
        message: `Arquivo fonte não encontrado: ${frontmatter.source}`,
        suggestion: `Verifique se ${sourcePath} existe`
      });
    }

    // CONT001: Description Length
    if (frontmatter.description) {
      const len = frontmatter.description.length;
      if (len < 50 || len > 160) {
        violations.push({
          ruleId: 'CONT001',
          severity: 'ERROR',
          file,
          message: `Descrição tem ${len} caracteres (esperado: 50-160)`,
          suggestion: len < 50 ? 'Expanda a descrição' : 'Reduza para máximo 160'
        });
      }
    }

    // CONT002: Title Present
    if (!frontmatter.title || frontmatter.title.trim() === '') {
      violations.push({
        ruleId: 'CONT002',
        severity: 'ERROR',
        file,
        message: 'Campo title é obrigatório e não pode ser vazio'
      });
    }
  }

  return {
    violations,
    stats: {
      filesChecked: files.length,
      errors: violations.filter(v => v.severity === 'ERROR').length,
      warnings: violations.filter(v => v.severity === 'WARNING').length,
      infos: violations.filter(v => v.severity === 'INFO').length
    }
  };
}
```

## Validação de Links

```typescript
async function validateLinks(): Promise<Violation[]> {
  const violations: Violation[] = [];
  const files = await glob('src/content/docs/**/*.mdx');

  const existingPages = new Set(
    files.map(f => f.replace('src/content/docs/', '/').replace('.mdx', '/'))
  );

  const linkPattern = /\[([^\]]+)\]\(([^)]+)\)/g;

  for (const file of files) {
    const content = await readFile(file, 'utf-8');
    const { content: body } = matter(content);

    let match;
    while ((match = linkPattern.exec(body)) !== null) {
      const [, , href] = match;

      if (href.startsWith('http') || href.startsWith('#') || href.startsWith('mailto:')) {
        continue;
      }

      const normalizedHref = href.endsWith('/') ? href : href + '/';
      if (!existingPages.has(normalizedHref) && !href.startsWith('/images/')) {
        violations.push({
          ruleId: 'CONT003',
          severity: 'ERROR',
          file,
          message: `Link quebrado: ${href}`,
          suggestion: 'Verifique se a página existe'
        });
      }
    }
  }

  return violations;
}
```

## Validação de Imagens

```typescript
async function validateImages(): Promise<Violation[]> {
  const violations: Violation[] = [];
  const files = await glob('src/content/docs/**/*.mdx');
  const imagePattern = /!\[([^\]]*)\]\(([^)]+)\)/g;

  for (const file of files) {
    const content = await readFile(file, 'utf-8');
    const { content: body } = matter(content);

    let match;
    while ((match = imagePattern.exec(body)) !== null) {
      const [, alt, src] = match;

      // CONT005: Alt Text Required
      if (!alt || alt.trim() === '') {
        violations.push({
          ruleId: 'CONT005',
          severity: 'WARNING',
          file,
          message: `Imagem sem texto alternativo: ${src}`,
          suggestion: 'Adicione descrição: ![descrição](url)'
        });
      }

      // CONT004: No Dead Images
      if (src.startsWith('/images/')) {
        const imagePath = path.join('public', src);
        if (!(await fileExists(imagePath))) {
          violations.push({
            ruleId: 'CONT004',
            severity: 'ERROR',
            file,
            message: `Imagem não encontrada: ${src}`,
            suggestion: `Verifique se ${imagePath} existe`
          });
        }
      }
    }
  }

  return violations;
}
```

## Função Main

```typescript
async function main() {
  console.log('Validando documentação WEBDOCS...\n');

  const sourceResult = await validateSources();
  const linkViolations = await validateLinks();
  const imageViolations = await validateImages();

  const allViolations = [
    ...sourceResult.violations,
    ...linkViolations,
    ...imageViolations
  ];

  const errors = allViolations.filter(v => v.severity === 'ERROR');
  const warnings = allViolations.filter(v => v.severity === 'WARNING');

  if (errors.length > 0) {
    console.log('ERROS:\n');
    errors.forEach(v => {
      console.log(`  [${v.ruleId}] ${v.file}`);
      console.log(`    ${v.message}`);
      if (v.suggestion) console.log(`    ${v.suggestion}`);
      console.log();
    });
  }

  if (warnings.length > 0) {
    console.log('AVISOS:\n');
    warnings.forEach(v => {
      console.log(`  [${v.ruleId}] ${v.file}: ${v.message}`);
    });
  }

  console.log('\nRESUMO:');
  console.log(`  Arquivos: ${sourceResult.stats.filesChecked}`);
  console.log(`  Erros: ${errors.length}`);
  console.log(`  Avisos: ${warnings.length}`);

  if (errors.length > 0) {
    process.exit(1);
  }
  process.exit(0);
}

main().catch(console.error);
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
