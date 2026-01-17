# Convenção de Status de Arquivo

Todo arquivo markdown em CENTRAL e PROJECTS deve incluir metadados de rodapé indicando seu estado atual de completude.

## Metadados Obrigatórios

O rodapé de cada arquivo deve conter campos separados por linha horizontal. O campo Última atualização indica a data da última modificação no formato AAAA-MM-DD. O campo Status do arquivo indica o estado atual com um dos três valores permitidos, sendo obrigatório apenas para READMEs. O campo Descrição é obrigatório apenas quando o status não for Pronto, explicando o que falta para conclusão.

## Metadados de ADR

Architecture Decision Records possuem metadados específicos além dos padrões. O campo Data indica quando a decisão foi tomada no formato AAAA-MM-DD. O campo Status indica o estado da decisão com valores como Proposto, Aprovado, Aprovado e Implementado, Deprecado ou Substituído. O campo Decisor indica quem tomou a decisão, podendo ser nome individual ou Equipe de Arquitetura.

## Valores de Status

O status Pronto indica que o arquivo está completo, revisado por humano e aprovado, podendo ser considerado fonte confiável de informação. O status Review indica que o arquivo foi gerado ou corrigido automaticamente e aguarda revisão humana para aprovação final. O status Incompleto indica que o arquivo existe mas possui conteúdo faltante, seja aguardando geração automática por script, seja aguardando redação manual de seções específicas. O status Errado indica que a estrutura do arquivo viola as convenções estabelecidas e precisa ser refatorado, seja por ter conteúdo que deveria estar fragmentado em arquivos filhos, seja por não seguir o padrão de seus irmãos.

## Formato

O rodapé segue o padrão com linha horizontal seguida dos campos em negrito. O campo Última atualização vem primeiro com a data. O campo Status do arquivo vem em seguida com o valor para READMEs. O campo Descrição aparece apenas para status Incompleto ou Errado explicando a pendência. Documentos com mais de 12 meses sem atualização são considerados desatualizados e devem ser revisados.

## Exemplos de Descrições

Para arquivos aguardando índice gerado automaticamente usar Aguardando index gerado por script. Para arquivos que precisam de mais conteúdo manual usar Aguardando redação da seção X. Para arquivos com estrutura errada usar explicação do que precisa mudar como O README deve ter somente parágrafo denso e o conteúdo deve ser fragmentado em arquivos numerados.

## Validação

Os scripts em .scripts/carf_validator validam automaticamente a presença dos metadados obrigatórios e reportam arquivos sem rodapé ou com formato incorreto. Os códigos de erro META001 a META006 identificam problemas específicos de metadados.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review
