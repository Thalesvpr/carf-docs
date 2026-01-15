---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: compatibility
---

# RF-200: Exportar Unidades em CSV

O sistema possibilita exportação de dados tabulares de unidades em formato CSV (Comma-Separated Values) que omite geometrias espaciais mas preserva todos os atributos alfanuméricos, sendo formato ideal para análises estatísticas, importação em planilhas eletrônicas como Excel ou Google Sheets, e integração com sistemas não geoespaciais que requerem apenas dados descritivos. A exportação inclui todas as colunas relevantes de unidades como identificador, código cadastral, tipo de ocupação, área calculada, status de aprovação, datas de cadastramento e atualização, além de informações relacionadas como nomes de titulares concatenados e endereço da unidade, fornecendo dataset abrangente para análises alfanuméricas. O arquivo gerado utiliza encoding UTF-8 com BOM (Byte Order Mark) que garante correta visualização de caracteres acentuados e especiais em ferramentas que suportam Unicode, evitando problemas comuns de encoding que resultam em caracteres corrompidos ao abrir CSVs brasileiros em software internacional. O sistema permite configuração do separador utilizado, oferecendo opções como vírgula (padrão internacional), ponto-e-vírgula (padrão brasileiro que evita conflitos com vírgulas decimais), tabulação ou outros caracteres, adaptando exportação a requisitos específicos de software de destino e preferências regionais de formatação numérica.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
