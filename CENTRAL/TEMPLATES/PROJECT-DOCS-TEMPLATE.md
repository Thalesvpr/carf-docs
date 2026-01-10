# Template de Documentação de Projeto CARF

Este template define a estrutura OBRIGATÓRIA de documentação que TODOS os projetos CARF devem ter antes de iniciar a implementação.

## 🎯 Princípio

> **"Um projeto deve se explicar completamente através da sua documentação antes de uma única linha de código ser escrita."**

---

## 📁 Estrutura Obrigatória

```
PROJECTS/{NOME-PROJETO}/
├── DOCS/
│   ├── README.md ⭐ OBRIGATÓRIO
│   ├── ARCHITECTURE/
│   │   ├── README.md ⭐ OBRIGATÓRIO
│   │   ├── 01-overview.md ⭐ OBRIGATÓRIO
│   │   ├── 02-layers.md (se aplicável)
│   │   ├── 03-data-flow.md ⭐ OBRIGATÓRIO
│   │   ├── 04-integration.md ⭐ OBRIGATÓRIO
│   │   └── 05-deployment.md ⭐ OBRIGATÓRIO
│   ├── CONCEPTS/
│   │   ├── README.md ⭐ OBRIGATÓRIO
│   │   ├── 01-key-concepts.md ⭐ OBRIGATÓRIO
│   │   ├── 02-terminology.md ⭐ OBRIGATÓRIO
│   │   └── 03-design-principles.md ⭐ OBRIGATÓRIO
│   ├── HOW-TO/
│   │   ├── README.md ⭐ OBRIGATÓRIO
│   │   ├── 01-setup-dev-environment.md ⭐ OBRIGATÓRIO
│   │   ├── 02-build-and-run.md ⭐ OBRIGATÓRIO
│   │   ├── 03-testing.md ⭐ OBRIGATÓRIO
│   │   └── 04-troubleshooting.md ⭐ OBRIGATÓRIO
│   └── API/ (se aplicável - para libs/backends)
│       ├── README.md ⭐ OBRIGATÓRIO
│       └── reference.md ⭐ OBRIGATÓRIO
└── SRC-CODE/{nome-repo}/
    └── README.md ⭐ OBRIGATÓRIO
```

---

## 📄 Conteúdo Obrigatório por Arquivo

### 1. `DOCS/README.md` ⭐

**Propósito:** Ponto de entrada da documentação do projeto.

**Deve conter:**
```markdown
# {NOME-PROJETO} - Documentação

## Visão Geral
[Parágrafo explicando o que é o projeto, seu propósito no ecossistema CARF]

## Estrutura da Documentação
### ARCHITECTURE/
[Lista de documentos com 1 linha de descrição cada]

### CONCEPTS/
[Lista de documentos com 1 linha de descrição cada]

### HOW-TO/
[Lista de documentos com 1 linha de descrição cada]

### API/ (se aplicável)
[Lista de documentos com 1 linha de descrição cada]

## Relação com CENTRAL/
[Links para documentação central relevante]

## Relação com outros projetos
### Dependências
[Projetos dos quais este depende, com links]

### Consumidores
[Projetos que consomem este, com links]

## Tecnologias
[Lista de tecnologias principais com versões]

## Quick Start
[Comando rápido para rodar o projeto]

## Links Úteis
[Links para CENTRAL, ADRs, outros projetos]
```

---

### 2. `DOCS/ARCHITECTURE/README.md` ⭐

**Propósito:** Índice da documentação arquitetural.

**Deve conter:**
```markdown
# Arquitetura - {NOME-PROJETO}

## Documentos Disponíveis

| Documento | Descrição |
|-----------|-----------|
| `01-overview.md` | Visão geral da arquitetura |
| `02-layers.md` | Camadas e responsabilidades |
| `03-data-flow.md` | Fluxo de dados no sistema |
| `04-integration.md` | Integrações com outros sistemas |
| `05-deployment.md` | Arquitetura de deployment |

## ADRs Relacionados
[Links para ADRs do CENTRAL que se aplicam a este projeto]

## Decisões Arquiteturais Específicas
[Decisões arquiteturais específicas deste projeto]
```

---

### 3. `DOCS/ARCHITECTURE/01-overview.md` ⭐

**Propósito:** Visão geral da arquitetura do projeto.

**Deve conter:**
```markdown
# Overview da Arquitetura - {NOME-PROJETO}

## Visão Geral
[Parágrafo explicando a arquitetura em alto nível]

## Diagrama de Arquitetura
[Diagrama mostrando componentes principais e suas relações]

## Componentes Principais
### Componente 1
[Descrição, responsabilidades]

### Componente 2
[Descrição, responsabilidades]

## Padrões Arquiteturais Utilizados
- [Pattern 1] - [Justificativa]
- [Pattern 2] - [Justificativa]

## Princípios de Design
- [Princípio 1]
- [Princípio 2]

## Decisões Técnicas Chave
### Tecnologia A vs Tecnologia B
[Por que escolhemos A]

## Stack Tecnológico
| Camada | Tecnologia | Versão | Justificativa |
|--------|------------|--------|---------------|
| ... | ... | ... | ... |

## Referências
- `ADR-XXX` (Link para ADR relevante)
- `CENTRAL/ARCHITECTURE/PATTERNS/` (Link para padrões arquiteturais)
```

---

### 4. `DOCS/ARCHITECTURE/03-data-flow.md` ⭐

**Propósito:** Explicar como os dados fluem no sistema.

**Deve conter:**
```markdown
# Fluxo de Dados - {NOME-PROJETO}

## Visão Geral
[Como os dados entram, são processados e saem do sistema]

## Diagramas de Fluxo

### Fluxo 1: [Nome do Fluxo]
[Diagrama ou descrição textual]

**Entrada:** [O que entra]
**Processamento:** [O que acontece]
**Saída:** [O que sai]

### Fluxo 2: [Nome do Fluxo]
[...]

## Transformações de Dados
[Como os dados são transformados entre camadas]

## Persistência de Dados
[Onde e como os dados são armazenados]

## Validação de Dados
[Onde e como os dados são validados]

## Exemplos
### Exemplo 1: [Cenário Real]
[Passo a passo do fluxo de dados]
```

---

### 5. `DOCS/ARCHITECTURE/04-integration.md` ⭐

**Propósito:** Documentar todas as integrações externas.

**Deve conter:**
```markdown
# Integrações - {NOME-PROJETO}

## Visão Geral
[Resumo das integrações]

## Dependências

### Sistema A
- **Tipo:** REST API / gRPC / GraphQL / Lib
- **Propósito:** [Para que usamos]
- **Documentação:** [Link]
- **Autenticação:** [Como autenticamos]
- **Endpoints usados:** [Lista]
- **Fallback:** [O que acontece se cair]

### Sistema B
[...]

## Consumidores
[Quem consome este projeto e como]

## Diagrama de Integração
[Diagrama mostrando todas as integrações]

## Contratos de Interface
[Se este projeto expõe APIs, listar contratos]

## Autenticação & Autorização
[Como este projeto se autentica com dependências]
[Como consumidores se autenticam com este projeto]

## Tratamento de Erros
[Como erros de integração são tratados]

## Monitoramento
[Como integrações são monitoradas]
```

---

### 6. `DOCS/ARCHITECTURE/05-deployment.md` ⭐

**Propósito:** Arquitetura de deployment e infraestrutura.

**Deve conter:**
```markdown
# Deployment - {NOME-PROJETO}

## Visão Geral
[Como o projeto é deployado]

## Ambientes

### Development
- **Onde:** [Local / Docker / Cloud]
- **URL:** [Se aplicável]
- **Configuração:** [Variáveis de ambiente necessárias]

### Staging
- **Onde:** [Cloud provider, região]
- **URL:** [URL]
- **Configuração:** [Vars]

### Production
- **Onde:** [Cloud provider, região]
- **URL:** [URL]
- **Configuração:** [Vars]

## Infraestrutura

### Containerização
- **Dockerfile:** [Localização]
- **Imagem base:** [Qual imagem]
- **Multi-stage build:** [Sim/Não]

### Orquestração
- **Kubernetes:** [Sim/Não]
- **Manifests:** [Localização]
- **Recursos:** [CPU, RAM necessários]

### Networking
- **Portas expostas:** [Lista]
- **Load balancer:** [Tipo]
- **CDN:** [Se aplicável]

## CI/CD

### Pipeline
- **Ferramenta:** GitHub Actions / GitLab CI / etc
- **Arquivo:** [Localização do pipeline]
- **Triggers:** [O que dispara deploy]

### Build
[Como fazer build]

### Testes
[Quais testes rodam no CI]

### Deploy
[Como é feito deploy]

## Secrets & Config
- **Secrets Manager:** [Qual]
- **Variáveis de ambiente:** [Lista com descrição]

## Backup & Recovery
- **Estratégia de backup:** [Se aplicável]
- **RPO:** [Recovery Point Objective]
- **RTO:** [Recovery Time Objective]

## Escalabilidade
- **Horizontal scaling:** [Sim/Não, como]
- **Vertical scaling:** [Limites]
- **Auto-scaling:** [Configurado?]

## Monitoramento
- **Logs:** [Onde, como acessar]
- **Métricas:** [Grafana, Prometheus, etc]
- **Alertas:** [Configurados onde]

## Disaster Recovery
[Plano de contingência]
```

---

### 7. `DOCS/CONCEPTS/README.md` ⭐

**Propósito:** Índice dos conceitos fundamentais.

**Deve conter:**
```markdown
# Conceitos - {NOME-PROJETO}

## Documentos Disponíveis

| Documento | Descrição |
|-----------|-----------|
| `01-key-concepts.md` | Conceitos chave do domínio |
| `02-terminology.md` | Glossário de termos |
| `03-design-principles.md` | Princípios de design |

## Para quem é esta seção
Esta seção é para desenvolvedores que precisam entender os conceitos fundamentais antes de começar a trabalhar no código.
```

---

### 8. `DOCS/CONCEPTS/01-key-concepts.md` ⭐

**Propósito:** Explicar conceitos fundamentais do domínio.

**Deve conter:**
```markdown
# Conceitos Chave - {NOME-PROJETO}

## Conceito 1: [Nome]
[Explicação clara e concisa]

**Por que é importante:** [Relevância]
**Como se relaciona com o código:** [Onde aparece no código]

## Conceito 2: [Nome]
[...]

## Conceitos do Domínio CARF
[Conceitos específicos de regularização fundiária que este projeto usa]

## Referências
- `CENTRAL/DOMAIN-MODEL/` (Modelo de domínio central)
- `CENTRAL/BUSINESS-RULES/` (Regras de negócio central)
```

---

### 9. `DOCS/CONCEPTS/02-terminology.md` ⭐

**Propósito:** Glossário de termos usados no projeto.

**Deve conter:**
```markdown
# Terminologia - {NOME-PROJETO}

## Glossário

### Termo A
**Definição:** [Definição clara]
**Sinônimos:** [Se houver]
**Exemplo:** [Uso no contexto do projeto]
**Ver também:** [Termos relacionados]

### Termo B
[...]

## Termos do Domínio CARF
[Links para glossário central se houver]

## Abreviações
| Abrev. | Significado |
|--------|-------------|
| RF | Requisito Funcional |
| UC | Use Case |
| ... | ... |
```

---

### 10. `DOCS/CONCEPTS/03-design-principles.md` ⭐

**Propósito:** Princípios de design que guiam o desenvolvimento.

**Deve conter:**
```markdown
# Princípios de Design - {NOME-PROJETO}

## Princípios Gerais

### Princípio 1: [Nome]
**Descrição:** [O que é]
**Justificativa:** [Por que adotamos]
**Como aplicar:** [Exemplo prático]

### Princípio 2: [Nome]
[...]

## Princípios Específicos do Projeto
[Princípios únicos deste projeto]

## Anti-patterns a Evitar
- [Anti-pattern 1]: [Por que evitar]
- [Anti-pattern 2]: [Por que evitar]

## Code Style Guidelines
[Link para style guide ou resumo]

## Referências
- Clean Code (link exemplo)
- DDD (link exemplo)
- CENTRAL/ARCHITECTURE/PATTERNS/ (link exemplo)
```

---

### 11. `DOCS/HOW-TO/README.md` ⭐

**Propósito:** Índice de guias práticos.

**Deve conter:**
```markdown
# How-To Guides - {NOME-PROJETO}

## Documentos Disponíveis

| Documento | Descrição |
|-----------|-----------|
| `01-setup-dev-environment.md` | Como configurar ambiente de desenvolvimento |
| `02-build-and-run.md` | Como fazer build e rodar o projeto |
| `03-testing.md` | Como rodar e escrever testes |
| `04-troubleshooting.md` | Solução de problemas comuns |

## Para quem são estes guias
Guias práticos para desenvolvedores que precisam realizar tarefas específicas.
```

---

### 12. `DOCS/HOW-TO/01-setup-dev-environment.md` ⭐

**Propósito:** Instruções passo a passo para configurar ambiente de dev.

**Deve conter:**
```markdown
# Setup do Ambiente de Desenvolvimento - {NOME-PROJETO}

## Pré-requisitos

### Software Necessário
- [ ] [Software 1] versão X.Y.Z ou superior
- [ ] [Software 2] versão X.Y.Z ou superior
- [ ] [...]

### Contas/Acessos Necessários
- [ ] Acesso ao GitHub
- [ ] [Outras contas necessárias]

## Passo a Passo

### 1. Clone do Repositório
```bash
git clone [URL]
cd [diretório]
```

### 2. Instalar Dependências
```bash
[comando de instalação]
```

### 3. Configurar Variáveis de Ambiente
```bash
cp .env.example .env
# Editar .env com:
# - VAR1=valor1
# - VAR2=valor2
```

### 4. Configurar Banco de Dados (se aplicável)
```bash
[comandos]
```

### 5. Rodar Migrations (se aplicável)
```bash
[comandos]
```

### 6. Verificar Instalação
```bash
[comando para verificar que tudo está OK]
```

## Configuração de IDE

### VSCode
- Extensões recomendadas: [lista]
- Settings: [configurações]

### JetBrains IDEs
[...]

## Troubleshooting
[Problemas comuns durante setup e soluções]

## Próximos Passos
- `02-build-and-run.md` (Guia de build e execução)
```

---

### 13. `DOCS/HOW-TO/02-build-and-run.md` ⭐

**Propósito:** Como fazer build e executar o projeto.

**Deve conter:**
```markdown
# Build e Run - {NOME-PROJETO}

## Desenvolvimento

### Build
```bash
[comando de build]
```

### Run
```bash
[comando para rodar]
```

### Hot Reload / Watch Mode
```bash
[comando para desenvolvimento com auto-reload]
```

### Acessar a aplicação
- **URL:** http://localhost:XXXX
- **Credenciais padrão:** [se aplicável]

## Produção

### Build Otimizado
```bash
[comando de build production]
```

### Run Production Build
```bash
[comando para rodar build de produção localmente]
```

## Docker

### Build da Imagem
```bash
docker build -t {nome-projeto}:latest .
```

### Run Container
```bash
docker run -p XXXX:XXXX {nome-projeto}:latest
```

### Docker Compose
```bash
docker-compose up
```

## Variáveis de Ambiente
[Lista de variáveis necessárias e seus valores padrão]

## Portas Utilizadas
- XXXX: [Descrição]
- YYYY: [Descrição]

## Logs
[Onde encontrar logs, como configurar nível de log]
```

---

### 14. `DOCS/HOW-TO/03-testing.md` ⭐

**Propósito:** Como rodar e escrever testes.

**Deve conter:**
```markdown
# Testing - {NOME-PROJETO}

## Rodar Testes

### Todos os Testes
```bash
[comando]
```

### Testes Unitários
```bash
[comando]
```

### Testes de Integração
```bash
[comando]
```

### Testes E2E
```bash
[comando]
```

### Com Coverage
```bash
[comando]
```

### Watch Mode
```bash
[comando para rodar testes em watch mode]
```

## Escrever Testes

### Estrutura de Testes
[Onde colocar arquivos de teste]

### Convenções de Nomenclatura
- Arquivos: [padrão]
- Suites: [padrão]
- Tests: [padrão]

### Template de Teste
```[linguagem]
[exemplo de teste bem escrito]
```

### Mocking
[Como fazer mocks, quando usar]

### Fixtures
[Onde ficam fixtures, como usar]

## Pirâmide de Testes
- XX% unit tests
- YY% integration tests
- ZZ% e2e tests

## Code Coverage
- **Target:** XX%
- **Reportes:** [Onde ver]

## CI/CD
[Quais testes rodam no CI, quando]

## Boas Práticas
- [Prática 1]
- [Prática 2]
```

---

### 15. `DOCS/HOW-TO/04-troubleshooting.md` ⭐

**Propósito:** Solução de problemas comuns.

**Deve conter:**
```markdown
# Troubleshooting - {NOME-PROJETO}

## Problemas Comuns

### Problema 1: [Descrição do erro]
**Sintomas:** [Como se manifesta]
**Causa:** [Por que acontece]
**Solução:**
```bash
[comandos ou passos para resolver]
```

### Problema 2: [...]
[...]

## Problemas de Instalação
[...]

## Problemas de Build
[...]

## Problemas de Runtime
[...]

## Problemas de Integração
[...]

## Logs e Debugging

### Ver Logs
```bash
[como acessar logs]
```

### Debug Mode
```bash
[como ativar debug]
```

### Breakpoints (se aplicável)
[Como usar debugger]

## Onde Pedir Ajuda
- **GitHub Issues:** [link]
- **Slack/Discord:** [canal]
- **Email:** [contato]

## Reportar Bugs
[Template de bug report]
```

---

### 16. `SRC-CODE/{nome-repo}/README.md` ⭐

**Propósito:** README do repositório de código (visto no GitHub).

**Deve conter:**
```markdown
# {NOME-PROJETO}

[Badge de build status]
[Badge de coverage]
[Badge de versão]

[Parágrafo curto descrevendo o projeto]

## 🚀 Quick Start

```bash
# Clone
git clone [url]

# Install
[comando de install]

# Run
[comando de run]
```

## 📚 Documentação

Documentação completa em: `../../DOCS/README.md`

- `../../DOCS/ARCHITECTURE/` (Documentação de arquitetura)
- `../../DOCS/CONCEPTS/` (Conceitos fundamentais)
- `../../DOCS/HOW-TO/` (Guias práticos)

## 🛠️ Stack

- [Tech 1] X.Y.Z
- [Tech 2] X.Y.Z

## 🔗 Links

- `../../../../CENTRAL/` (Documentação central do CARF)
- `../../../../PROJECTS/` (Outros projetos relacionados)

## 📄 License

UNLICENSED - Proprietary

## 🤝 Contributing

[Guidelines ou link para CONTRIBUTING.md]
```

---

## ✅ Checklist de Completude

Use esta checklist para verificar se um projeto tem documentação completa:

### Arquitetura
- [ ] README.md
- [ ] 01-overview.md
- [ ] 03-data-flow.md
- [ ] 04-integration.md
- [ ] 05-deployment.md

### Conceitos
- [ ] README.md
- [ ] 01-key-concepts.md
- [ ] 02-terminology.md
- [ ] 03-design-principles.md

### How-To
- [ ] README.md
- [ ] 01-setup-dev-environment.md
- [ ] 02-build-and-run.md
- [ ] 03-testing.md
- [ ] 04-troubleshooting.md

### Código
- [ ] SRC-CODE/README.md

**TOTAL:** 16 arquivos obrigatórios mínimos

---

## 🎯 Regra de Ouro

> **Nenhum código pode ser escrito antes de todos os ⭐ OBRIGATÓRIOS estarem completos.**

Isso garante que:
- Todos entendem o que será construído
- Decisões arquiteturais foram pensadas
- Novos desenvolvedores conseguem começar rapidamente
- Há rastreabilidade de decisões

---

## 📝 Notas

- Projetos podem ter documentação ADICIONAL além desta estrutura mínima
- A estrutura mínima é **não-negociável**
- Documentação deve ser atualizada junto com o código
- PRs sem atualização de docs devem ser rejeitados

---

**Criado em:** 2026-01-09
**Versão:** 1.0
