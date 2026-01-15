---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: security
---

# UC-009-FA-002: Assinatura Digital do Termo

Fluxo alternativo do UC-009 Gerenciar Processo de Legitimação desviando no passo 14.5 onde ao invés de apenas baixar PDF para assinatura física manual, usuário clica botão Assinar Digitalmente disparando integração com plataforma de assinatura eletrônica qualificada como DocuSign D4Sign ou ClickSign via API REST, sistema envia POST request à plataforma contendo PDF do termo emails dos signatários requeridos (beneficiário gestor municipal técnico responsável se REURB-E) e callback URL para notificação de conclusão, plataforma retorna signing_session_id e URLs individuais para cada signatário acessar interface de assinatura, sistema envia emails automáticos via SMTP para cada signatário contendo link personalizado com token de autenticação e instruções sobre como assinar usando certificado digital ICP-Brasil A1 ou A3 ou assinatura eletrônica simples conforme nível de validação configurado no tenant, signatários acessam links clicam em áreas demarcadas do documento inserem certificado digital ou assinam com biometria facial smartphone, após todos assinarem plataforma envia webhook POST para callback URL notificando conclusão com signed_document_url apontando para PDF final com assinaturas embutidas e carimbos de tempo, sistema baixa PDF assinado salva em object storage sobrescrevendo versão não assinada atualiza process_documents com signed=true signed_at=NOW() signer_emails JSON, exibe badge verde Assinado Digitalmente na tela de processo mostrando data e signatários, PDF assinado possui validade jurídica equivalente a assinatura manuscrita conforme MP 2.200-2/2001 e Lei 14.063/2020 sendo aceito em cartórios para registro de imóveis eliminando necessidade de comparecimento presencial economizando tempo e facilitando regularização em municípios remotos onde beneficiários têm dificuldade de deslocamento até sede administrativa.

**Ponto de Desvio:** Passo 14.5 do UC-009 (após gerar PDF, antes de baixar)

**Retorno:** PDF assinado digitalmente com validade jurídica, processo atualizado

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
