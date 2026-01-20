# Configuração de Organização

Estrutura organizacional do GitHub para o projeto CARF definindo times, permissões e políticas de acesso que garantem segurança e colaboração eficiente entre desenvolvedores.

## Times e Permissões

O projeto organiza colaboradores em times com responsabilidades específicas. Cada time tem acesso de escrita apenas aos repositórios sob sua responsabilidade e acesso de leitura aos demais para facilitar code review e colaboração cross-functional.

| Time | Repositórios (Write) | Membros |
|------|---------------------|---------|
| Backend Team | carf-geoapi, carf-keycloak | Desenvolvedores .NET e Java |
| Frontend Team | carf-geoweb, carf-tscore | Desenvolvedores React/TypeScript |
| Mobile Team | carf-reurbcad | Desenvolvedores React Native |
| GIS Team | carf-geogis | Desenvolvedores Python/QGIS |
| Docs Team | carf-webdocs, carf-docs | Tech Writers e documentadores |
| Admin Team | carf-admin | Desenvolvedores Next.js |
| Maintainers | Todos os repositórios | Tech Leads e arquitetos |

## Níveis de Acesso

GitHub oferece cinco níveis de permissão para repositórios. O projeto utiliza Read para colaboradores externos e stakeholders que precisam apenas visualizar código. Write é atribuído a desenvolvedores ativos do time responsável pelo repositório. Maintain é reservado para tech leads que gerenciam issues, PRs e releases. Admin é restrito a proprietários do projeto para configurações sensíveis.

## Políticas de Acesso

Novos colaboradores são adicionados ao time apropriado conforme seu perfil. O convite é enviado pelo maintainer do repositório usando gh api ou interface web. O colaborador deve aceitar o convite para obter acesso. Colaboradores inativos por mais de 90 dias são removidos automaticamente por política de segurança.

## Configuração de Time via CLI

Para adicionar membro a um time usar comando gh api especificando endpoint /orgs/OWNER/teams/TEAM/memberships/USERNAME com método PUT. Para listar membros de um time usar gh api /orgs/OWNER/teams/TEAM/members. Para remover membro usar DELETE no endpoint de membership.

## Audit Log

GitHub mantém log de auditoria de todas as ações administrativas incluindo adição e remoção de membros, mudanças de permissão, criação e exclusão de repositórios. Maintainers devem revisar o audit log mensalmente para detectar atividades suspeitas ou não autorizadas.

---

**Status:** Review
**Atualizado:** 2026-01-20
**Descrição:**
