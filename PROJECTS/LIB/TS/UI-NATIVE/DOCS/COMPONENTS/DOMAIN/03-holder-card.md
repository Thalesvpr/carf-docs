---
type: leaf
status: review
updated: 2026-01-24
---

# HolderCard

Componente que exibe dados de titular com formatacao de documentos.

## Props

Prop holder recebe objeto Holder de @carf/tscore/types. Prop onPress callback executado ao tocar no card. Prop variant aceita default ou compact. Prop showContact boolean controla exibicao de telefone e email.

## Dados Exibidos

Nome completo como titulo principal. CPF formatado via value object CPF.format exibindo mascara padrao. Tipo de entidade indicado via badge PESSOA_FISICA ou PESSOA_JURIDICA. CNPJ formatado quando titular e pessoa juridica.

## Formatacao de Documentos

CPF e CNPJ usam value objects de @carf/tscore/validations para formatacao consistente. Mascara aplicada automaticamente. Dados armazenados sem mascara, exibidos com mascara. Validacao implicita ao usar value objects.

## Informacoes de Contato

Quando showContact true, exibe telefone e email. Telefone formatado com DDD entre parenteses. Email truncado se muito longo. Icones indicam tipo de contato.

## Variantes

Variante default mostra todas informacoes com Avatar. Variante compact oculta contato e usa layout horizontal. Avatar usa iniciais do nome como fallback. Cores de avatar determinadas por hash do nome.

## Interacao

Tap navega para detalhes do titular. Contatos permitem acao direta como ligar ou enviar email. Long press abre menu com opcoes adicionais. Visual feedback consistente com UnitCard.

## Acessibilidade

Nome e CPF formatado no accessibilityLabel. Tipo de entidade anunciado. Contatos focaveis individualmente. Actions secundarias acessiveis via menu contextual.
