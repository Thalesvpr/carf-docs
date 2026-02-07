---
type: adr
status: approved
updated: 2026-02-07
---

# ADR-004: React Hook Form com Zod para Formularios

## Contexto

O REURBCAD contem formularios complexos de cadastro de unidades e titulares com campos condicionais (conjuge obrigatorio se casado, foto obrigatoria se ausente), mascaras de input (CPF, data, telefone), validacao em tempo real com feedback visual imediato, e necessidade de preservar rascunhos durante navegacao entre steps de um wizard multi-etapa. Performance e critica pois o formulario de titular tem mais de 15 campos e o usuario opera em dispositivos Android de entrada com recursos limitados.

## Decisao

React Hook Form como biblioteca de formularios combinada com Zod para definicao e validacao de schemas. Cada formulario do app tem um Zod schema correspondente que define tipos, obrigatoriedades e regras de validacao. O React Hook Form consome esse schema via resolver @hookform/resolvers/zod, unificando tipagem TypeScript e validacao runtime em uma unica fonte de verdade.

Validacao executada em dois momentos. No onChange, validacao individual do campo modificado para feedback visual imediato: borda vermelha e mensagem de erro aparecem assim que o usuario sai do campo com valor invalido, permitindo correcao antes de tentar submeter. No onSubmit, validacao completa do schema inteiro para capturar regras cruzadas entre campos, como a obrigatoriedade de dados do conjuge quando estado civil e casado ou uniao estavel.

Erros exibidos inline imediatamente abaixo de cada campo em texto vermelho com fonte tamanho 12px. Campos invalidos recebem borda vermelha. Campos validados com sucesso recebem borda verde. O botao de submit permanece habilitado mas, se pressionado com erros, a tela rola automaticamente ate o primeiro campo invalido.

Mascaras de input implementadas com bibliotecas de formatacao que intercetam o onChange do React Hook Form: CPF formatado como 000.000.000-00 com validacao de digitos verificadores Mod11, data formatada como DD/MM/AAAA com validacao de data valida, telefone formatado como (00) 00000-0000. O valor armazenado no form state e sempre o valor limpo sem mascara (CPF como 11 digitos, data como ISO 8601).

Integracao com useFormStore do Zustand para persistencia de rascunho: a cada alteracao relevante no formulario (debounce de 2 segundos), o estado atual do form e serializado e salvo na store. Ao retornar para o formulario apos navegacao, o React Hook Form e reinicializado com os valores do rascunho via defaultValues. Ao finalizar o cadastro com sucesso, o rascunho e limpo da store.

## Justificativa

React Hook Form usa inputs uncontrolled por padrao, evitando re-render de todos os campos a cada keystroke. Isso e critico em dispositivos Android de entrada onde re-renders frequentes causam jank perceptivel no teclado. O bundle de React Hook Form e 8.6KB gzipped e o de Zod e 13KB gzipped, ambos compactos para mobile. A combinacao elimina duplicacao entre tipos TypeScript e regras de validacao pois Zod schemas geram tipos automaticamente via z.infer.

## Alternativas Descartadas

Formik descartado por usar controlled inputs que causam re-render em cascata a cada keystroke, problema critico em formularios com 15 ou mais campos em dispositivos de entrada. Yup descartado como biblioteca de validacao por inferencia de tipos TypeScript inferior ao Zod e API menos composivel para validacoes condicionais complexas. Validacao manual sem biblioteca descartada por exigir reimplementacao de logica de dirty tracking, touched state, error aggregation e scroll-to-error disponivel out-of-the-box no React Hook Form.
