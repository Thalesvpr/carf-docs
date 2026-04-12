---
type: adr
status: accepted
updated: 2026-02-07
description: "Decisao sobre lifetimes de tokens e configuracao de sessoes no Keycloak CARF."
---

# ADR-003: Token Lifetimes e Session Configuration

## Contexto

Tempo de vida de tokens impacta diretamente seguranca e usabilidade. Tokens longos melhoram a experiencia mas aumentam a janela de exposicao em caso de vazamento. Tokens curtos sao mais seguros mas causam interrupcoes frequentes. O CARF atende cenarios distintos: analistas em escritorio trabalhando longas horas, agentes de campo com conectividade intermitente e servicos M2M executando operacoes batch.

## Decisao

Access token expira em cinco minutos para minimizar janela de exposicao. SSO session idle expira em trinta minutos e session max em dez horas. Remember me estende idle para um dia e max para sete dias. Offline session idle de trinta dias atende REURBCAD em campo. Refresh token rotation obrigatoria com max reuse zero garante que cada refresh token so pode ser usado uma unica vez, invalidando o anterior apos uso.

## Consequencias

Access token curto limita exposicao enquanto refresh silencioso mantem a sessao sem interrupcao para o usuario. Offline tokens de trinta dias permitem agentes de campo operar em areas remotas por periodos estendidos. Rotation detecta comprometimento quando atacante e usuario legitimo tentam refresh simultaneamente. Sessoes ociosas expiram automaticamente reduzindo risco de sessoes abandonadas. Em contrapartida, refresh a cada quatro a cinco minutos adiciona carga no Keycloak e frontends precisam implementar interceptor para refresh automatico. Tokens offline requerem secure storage adequado em mobile.

## Alternativas Rejeitadas

Access token longo de uma hora ou mais foi rejeitado porque token vazado permaneceria valido por tempo excessivo e access tokens stateless nao podem ser revogados individualmente. Sem refresh token rotation foi rejeitado porque token roubado poderia ser usado indefinidamente ate expirar. SSO session infinita foi rejeitada porque usuarios que esquecem logout permaneceriam autenticados indefinidamente sem verificacao periodica de credenciais.
