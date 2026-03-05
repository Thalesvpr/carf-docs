# CARF Keycloak Theme - JavaScript Resources

Este diretório contém os scripts JavaScript utilizados no tema de login do Keycloak.

## Arquivos

### 1. carf-validations.js (Browser Bundle do @carf/tscore)

**Origem**: `@carf/tscore` - Biblioteca compartilhada TypeScript do ecossistema CARF
**Localização Source**: `PROJECTS/LIB/TS/TSCORE/SRC-CODE/carf-tscore`
**Build**: `bun run build:browser`
**Tamanho**: ~4.3 KB (minificado)

**Conteúdo**:
- Validação de CPF (dígito verificador completo)
- Validação de CNPJ
- Validação de Email
- Validação de Phone
- Formatadores para todos os tipos acima
- Normalizadores (remove formatação)

**API Global** (disponível como `window.CarfValidations`):

```javascript
// Classes (Value Objects)
CarfValidations.CPF
CarfValidations.CNPJ
CarfValidations.Email
CarfValidations.Phone
CarfValidations.ValidationError

// Utilitários (mais simples para uso no browser)
CarfValidations.Validators.cpf.validate('123.456.789-09') // boolean
CarfValidations.Validators.cpf.normalize('123.456.789-09') // '12345678909'
CarfValidations.Validators.cpf.format('12345678909') // '123.456.789-09'

CarfValidations.Validators.cnpj.validate('12.345.678/0001-90')
CarfValidations.Validators.cnpj.normalize('12.345.678/0001-90')
CarfValidations.Validators.cnpj.format('12345678000190')

CarfValidations.Validators.email.validate('usuario@example.com')

CarfValidations.Validators.phone.validate('(11) 98765-4321')
CarfValidations.Validators.phone.normalize('(11) 98765-4321')
CarfValidations.Validators.phone.format('11987654321')
```

**Quando Atualizar**:
Este arquivo deve ser regerado sempre que houver mudanças nas validações em `@carf/tscore`:

```bash
# No diretório carf-tscore
cd /c/DEV/CARF/PROJECTS/LIB/TS/TSCORE/SRC-CODE/carf-tscore

# Build do browser bundle
bun run build:browser

# Copiar para o tema Keycloak
cp dist/browser/carf-validations.js \
   /c/DEV/CARF/PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/themes/carf/login/resources/js/
```

---

### 2. login.js (UI e Interações)

**Propósito**: Gerencia interações de UI e aplicação das validações do tscore

**Funcionalidades**:
- ✅ Máscara automática de CPF no campo username
- ✅ Validação em tempo real de CPF (após 11 dígitos)
- ✅ Feedback visual (borda verde = válido, vermelha = inválido)
- ✅ Mensagens de erro acessíveis (ARIA)
- ✅ Suporte a paste (formata automaticamente)
- ✅ Animações suaves (fade-in, ripple effect)
- ✅ Melhorias de acessibilidade (roles, labels, ARIA attributes)

**Dependências**:
- Requer `carf-validations.js` carregado ANTES (definido em `theme.properties`)
- Graceful degradation: se bundle não carregar, CPF validation é desabilitado mas página funciona

**Não editar diretamente**: Este arquivo é acoplado ao bundle do tscore. Mantenha a lógica de validação no tscore.

---

## Ordem de Carregamento

Definida em `theme.properties`:

```properties
scripts=js/carf-validations.js js/login.js
```

**IMPORTANTE**: `carf-validations.js` DEVE vir antes de `login.js`!

## Padrão de Desenvolvimento

### ✅ BOM: Adicionar nova validação

1. Adicionar validação no `@carf/tscore/src/validations/`
2. Exportar em `src/validations-browser.ts`
3. Rebuild browser bundle: `bun run build:browser`
4. Copiar para Keycloak theme
5. Usar no `login.js` via `window.CarfValidations`

### ❌ RUIM: Reimplementar validação

Não duplique lógica de validação em `login.js`. Sempre use o bundle do tscore!

## Debugging

### Verificar se bundle carregou

Abra o Console do navegador:

```javascript
// Deve retornar objeto com CPF, CNPJ, Email, etc
window.CarfValidations

// Teste rápido
CarfValidations.Validators.cpf.validate('123.456.789-09')
// false (CPF inválido)

CarfValidations.Validators.cpf.validate('111.444.777-35')
// true (CPF válido)
```

### Logs

O `login.js` exibe logs no console:

```
✅ [CARF Theme] Loaded @carf/tscore validations successfully
```

Ou, se houver problema:

```
⚠️ [CARF Theme] @carf/tscore validations bundle not loaded. CPF validation will be disabled.
```

## Testes Manuais

### Teste 1: Validação de CPF válido
1. Abrir página de login
2. Digitar CPF válido: `111.444.777-35`
3. ✅ Borda deve ficar verde após 11 dígitos

### Teste 2: Validação de CPF inválido
1. Digitar CPF inválido: `123.456.789-09`
2. ❌ Borda deve ficar vermelha
3. Ao sair do campo, mensagem de erro deve aparecer

### Teste 3: Máscara automática
1. Digitar apenas números: `11144477735`
2. ✅ Deve formatar automaticamente para: `111.444.777-35`

### Teste 4: Paste
1. Copiar CPF: `11144477735`
2. Colar no campo username
3. ✅ Deve formatar e validar automaticamente

### Teste 5: Email/Username
1. Digitar email: `usuario@example.com`
2. ✅ Não deve aplicar máscara de CPF
3. ✅ Não deve mostrar erro

## Compatibilidade de Browsers

Testado e funcional em:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

**Recursos usados**:
- ES5 (gerado pelo Bun build com target: browser)
- window global
- DOM APIs padrão
- EventListener API

## Performance

**Bundle Size**: 4.34 KB minificado
**Parse Time**: < 5ms
**Memory**: < 100 KB

**Otimizações**:
- IIFE format (não precisa módulos)
- Minificado
- Tree-shaking aplicado pelo Bun
- Sem dependências externas

## Futuras Melhorias

### Possíveis adições ao bundle

1. **CNPJ Mask**: Aplicar máscara de CNPJ em campos específicos
2. **CEP Validation**: Validar CEPs brasileiros
3. **Phone Mask**: Máscara de telefone (11) 98765-4321
4. **Date Utils**: Formatação de datas brasileiras

### Componentes React

Se no futuro quisermos usar componentes React no Keycloak:

1. Adicionar React/ReactDOM ao bundle
2. Exportar componentes do tscore (ex: `<CPFInput />`)
3. Montar em elementos específicos da página

## Documentação Relacionada

- **@carf/tscore Source**: `PROJECTS/LIB/TS/TSCORE/SRC-CODE/carf-tscore/`
- **Validações Documentadas**: `CENTRAL/BUSINESS-RULES/VALIDATION-RULES/`
- **Keycloak Theme Docs**: `PROJECTS/KEYCLOAK/DOCS/`

## Manutenção

**Responsável**: Time de frontend CARF
**Frequência de Atualização**: Sempre que houver mudança em validações no tscore
**Testes**: Manuais (por enquanto) - ver seção "Testes Manuais" acima

## Suporte

Para problemas com:
- **Validações (lógica)**: Abrir issue no repositório `carf-tscore`
- **UI/UX (comportamento)**: Editar `login.js` neste diretório
- **Build/Bundle**: Verificar `package.json` scripts no `carf-tscore`

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Falta parágrafo denso introdutório; Falta seção GENERATED com índice automático; Muitas listas com bullets (6) antes do rodapé - considerar converter para parágrafo denso; Contém code blocks - considerar converter para prosa.

<!-- CARF-INDEX-START -->

<!-- CARF-INDEX-END -->
