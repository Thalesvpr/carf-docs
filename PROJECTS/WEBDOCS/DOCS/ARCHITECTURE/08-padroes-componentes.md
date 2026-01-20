# Padrões de Componentes

Especificação dos padrões para criação de componentes Astro no WEBDOCS, incluindo estrutura, props, estilos e hidratação.

## Estrutura de Componente Astro

Todo componente Astro segue estrutura com três seções: frontmatter (TypeScript), template (HTML/JSX), e estilos.

```json
{
  "component_structure": {
    "frontmatter": {
      "position": "Bloco --- no topo do arquivo",
      "language": "TypeScript",
      "contents": [
        "Interface Props",
        "Imports de dependências",
        "Lógica server-side",
        "Destructuring de Astro.props"
      ]
    },
    "template": {
      "position": "Após o frontmatter",
      "language": "HTML com expressões JSX",
      "rules": [
        "Usar Astro.props ou variáveis do frontmatter",
        "Slots para conteúdo filho",
        "class:list para classes condicionais"
      ]
    },
    "styles": {
      "position": "Tag <style> no final",
      "scope": "Scoped por padrão",
      "rules": [
        "Usar is:global apenas quando necessário",
        "Variáveis CSS para valores reutilizáveis",
        "Seguir design tokens de @carf/ui"
      ]
    }
  }
}
```

## Interface Props

Todo componente deve definir interface Props para tipagem.

```json
{
  "props_pattern": {
    "interface_name": "Props (sempre)",
    "common_props": {
      "class": {
        "type": "string",
        "required": false,
        "description": "Classes CSS adicionais"
      },
      "id": {
        "type": "string",
        "required": false,
        "description": "ID do elemento raiz"
      }
    },
    "destructuring": "const { prop1, prop2, class: className } = Astro.props"
  }
}
```

## Convenções de Naming

```json
{
  "naming": {
    "components": {
      "pattern": "PascalCase",
      "examples": ["StatusGrid", "UserMenu", "ServiceCard"]
    },
    "props_interface": {
      "pattern": "Props",
      "note": "Sempre usar 'Props', nunca 'IProps' ou 'ComponentProps'"
    },
    "css_classes": {
      "pattern": "kebab-case",
      "prefix": "Componente-específico ou nenhum",
      "examples": ["status-grid", "service-card", "user-menu-trigger"]
    },
    "css_variables": {
      "pattern": "--carf-{categoria}-{nome}",
      "examples": ["--carf-color-primary", "--carf-spacing-md"]
    }
  }
}
```

## Slots

Slots permitem passar conteúdo filho para componentes.

```json
{
  "slots": {
    "default": {
      "syntax": "<slot />",
      "usage": "Conteúdo principal passado como filho"
    },
    "named": {
      "syntax": "<slot name=\"header\" />",
      "usage": "Conteúdo específico para área nomeada"
    },
    "fallback": {
      "syntax": "<slot>Conteúdo padrão</slot>",
      "usage": "Conteúdo exibido se nenhum filho passado"
    }
  }
}
```

## Classes Condicionais

Usar class:list para classes condicionais.

```json
{
  "class_list": {
    "syntax": "class:list={[...]}",
    "patterns": {
      "static": "'classe-fixa'",
      "conditional": "{ 'classe': condition }",
      "dynamic": "variavel",
      "array": "['classe1', 'classe2']"
    },
    "example": "class:list={['base', { 'active': isActive }, className]}"
  }
}
```

## Diretivas de Hidratação

Componentes Astro são estáticos por padrão. Para interatividade client-side, usar diretivas de hidratação com componentes React.

```json
{
  "hydration_directives": {
    "none": {
      "usage": "Componentes puramente estáticos",
      "bundle_impact": "Zero JavaScript",
      "when": "Maioria dos componentes Astro"
    },
    "client:load": {
      "usage": "Hidrata imediatamente no load",
      "bundle_impact": "JavaScript carregado com a página",
      "when": "EVITAR - raramente necessário"
    },
    "client:idle": {
      "usage": "Hidrata quando browser está idle",
      "bundle_impact": "JavaScript carregado após interação inicial",
      "when": "PREFERIR para interatividade não-crítica"
    },
    "client:visible": {
      "usage": "Hidrata quando visível no viewport",
      "bundle_impact": "JavaScript carregado sob demanda",
      "when": "Componentes abaixo do fold ou pesados"
    },
    "client:only": {
      "usage": "Só renderiza no cliente",
      "bundle_impact": "Sem SSR, JavaScript obrigatório",
      "when": "Libs que não suportam SSR"
    }
  }
}
```

## Uso de Componentes React (@carf/ui)

Componentes React da biblioteca @carf/ui são importados e usados com diretivas de hidratação.

```json
{
  "react_components": {
    "import": "import { Button } from '@carf/ui'",
    "usage": "<Button client:idle onClick={handler}>Click</Button>",
    "rules": [
      "Sempre usar diretiva de hidratação",
      "Preferir client:idle ou client:visible",
      "Passar props como atributos",
      "Handlers como funções inline ou importadas"
    ]
  }
}
```

## Componentes Astro vs React

```json
{
  "decision_matrix": {
    "use_astro": [
      "Conteúdo estático",
      "Layout e estrutura",
      "Wrapper de componentes React",
      "Qualquer coisa sem interatividade"
    ],
    "use_react": [
      "Interatividade complexa (drag-drop, etc)",
      "Estado client-side",
      "Componentes @carf/ui",
      "Integrações com libs React"
    ]
  }
}
```

## Acessibilidade

```json
{
  "a11y_requirements": {
    "semantic_html": "Usar elementos semânticos (button, nav, main)",
    "aria_labels": "Adicionar aria-label quando necessário",
    "focus_management": "Garantir ordem de foco lógica",
    "keyboard_nav": "Todos elementos interativos acessíveis via teclado",
    "color_contrast": "Seguir WCAG 2.1 AA (4.5:1 para texto)"
  }
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
