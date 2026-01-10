# Requisitos Funcionais

O sistema CARF possui **222 requisitos funcionais** documentados, organizados por domínio e casos de uso.

## Organização

Os requisitos estão organizados em:

- **RF-001 a RF-050**: Gestão de Unidades Habitacionais
- **RF-051 a RF-100**: Gestão de Possuidores/Beneficiários
- **RF-101 a RF-150**: Gestão de Comunidades/Núcleos
- **RF-151 a RF-200**: Processos REURB
- **RF-201 a RF-222**: Integrações e Relatórios

## Consultar Requisitos

A documentação completa dos requisitos está disponível no repositório principal:

- [CENTRAL/REQUIREMENTS](https://github.com/Thalesvpr/carf-docs/tree/main/CENTRAL/REQUIREMENTS)

Cada requisito contém:

- **Identificador**: RF-XXX
- **Título**: Descrição curta
- **Descrição**: Detalhamento completo
- **Critérios de Aceitação**: Condições para validação
- **Regras de Negócio**: Restrições e validações
- **Tags**: Classificação por domínio, prioridade, etc.

## Exemplo de Requisito

```markdown
# RF-001 - Cadastrar Unidade Habitacional

**Tags**: #units #cadastro #p0

## Descrição
O sistema deve permitir o cadastro de unidades habitacionais...

## Critérios de Aceitação
- [ ] Formulário com todos os campos obrigatórios
- [ ] Validação de dados conforme regras de negócio
- [ ] Salvamento no banco de dados

## Regras de Negócio
- RN-001: CPF/CNPJ deve ser válido
- RN-002: Coordenadas geográficas obrigatórias
```

## Próximos Passos

- Ver [Casos de Uso](/docs/funcionalidades/)
- Consultar [API](/dev/api/)
- Entender a [Arquitetura](/dev/arquitetura/)
