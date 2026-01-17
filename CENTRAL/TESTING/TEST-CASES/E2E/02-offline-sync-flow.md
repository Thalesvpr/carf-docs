# Fluxo Offline Sync E2E

Testes end-to-end do fluxo de coleta offline e sincronização.

## TC-E2E-010: Coleta Offline Básica

```gherkin
Feature: Coleta de dados em campo sem conexão
  Como cadastrista em campo
  Quero cadastrar unidades mesmo sem internet
  Para que o trabalho em áreas remotas seja possível

Background:
  Dado que estou logado no app REURBCAD
  E sincronizei os dados iniciais do tenant

Cenário: Cadastrar unidade offline e sincronizar
  # Fase offline
  Dado que estou sem conexão com internet

  Quando acesso "Nova Unidade"
  E preencho o endereço manualmente
  E capturo coordenadas GPS
  E tiro 3 fotos com a câmera
  E salvo a unidade
  Então vejo a unidade na lista local com badge "Pendente sync"

  # Fase sync
  Quando reconecto à internet
  E clico em "Sincronizar"
  Então vejo progresso de upload
  E ao final, a unidade tem badge "Sincronizado"
  E a unidade aparece no sistema web
```

## TC-E2E-011: Conflito de Sincronização

```gherkin
Cenário: Resolver conflito de edição simultânea
  Dado que unidade X existe no servidor
  E baixei unidade X para offline

  Quando outro usuário edita unidade X no servidor
  E eu edito unidade X offline (campo diferente)
  E tento sincronizar

  Então vejo tela de "Conflito Detectado"
  E vejo comparativo das versões:
    | Campo    | Minha versão | Servidor |
    | Número   | 123          | 123      |
    | Bairro   | Centro (eu)  | Centro   |
    | Complemento | Apto 1 (eu) | Casa (servidor) |

  Quando escolho "Manter minha versão" para Complemento
  E clico em "Resolver Conflito"
  Então a unidade é sincronizada com minha versão do Complemento
```

## TC-E2E-012: Múltiplas Unidades Offline

```gherkin
Cenário: Cadastrar múltiplas unidades em batch
  Dado que estou offline

  Quando cadastro 10 unidades em sequência
  Então todas aparecem na fila de sync com "Pendente"

  Quando reconecto e sincronizo
  Então vejo barra de progresso "0/10... 5/10... 10/10"
  E todas as 10 unidades são enviadas
  E recebo relatório de sucesso
```

## TC-E2E-013: Falha Parcial de Sync

```gherkin
Cenário: Tratar falha em algumas unidades do batch
  Dado que tenho 5 unidades pendentes de sync
  E uma delas tem geometria inválida

  Quando sincronizo
  Então 4 unidades são sincronizadas com sucesso
  E 1 unidade falha com erro "Geometria inválida"
  E vejo opção de "Editar e Reenviar" para a unidade com erro
```

## TC-E2E-014: Fotos em Baixa Conectividade

```gherkin
Cenário: Upload de fotos com conexão instável
  Dado que tenho 3 fotos de 2MB cada pendentes
  E a conexão é 3G instável

  Quando inicio sincronização
  E a conexão cai no meio do upload da foto 2

  Então vejo "Upload pausado - aguardando conexão"

  Quando a conexão retorna
  Então o upload continua de onde parou
  E não há duplicação de fotos
```

## TC-E2E-015: Dados Expirados

```gherkin
Cenário: Alertar sobre dados offline muito antigos
  Dado que sincronizei há 7 dias
  E não tive conexão desde então

  Quando abro o app
  Então vejo alerta "Dados locais podem estar desatualizados"
  E opção "Sincronizar agora" ou "Continuar offline"
```

## Implementação de Testes

```typescript
// cypress/e2e/offline-sync.cy.ts
describe('Offline Sync', () => {
  beforeEach(() => {
    cy.login('cadastrista');
    cy.syncInitialData();
  });

  it('should create unit offline and sync when online', () => {
    // Go offline
    cy.intercept('**/api/**', { forceNetworkError: true }).as('offline');

    // Create unit
    cy.get('[data-testid="new-unit"]').click();
    cy.fillUnitForm(unitFixture);
    cy.get('[data-testid="save-offline"]').click();

    // Verify local storage
    cy.window().its('indexedDB').should('contain', 'pending_units');

    // Go online and sync
    cy.intercept('**/api/**').as('online');
    cy.get('[data-testid="sync-button"]').click();

    // Verify sync success
    cy.wait('@online');
    cy.get('[data-testid="sync-status"]').should('contain', 'Sincronizado');
  });
});
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
