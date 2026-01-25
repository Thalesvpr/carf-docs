---
type: glossary
status: approved
updated: 2026-01-25
category: conceitos
---

# Conceitos Principais

Definicoes dos conceitos fundamentais do sistema CARF.

## Ortofoto

Mosaico georreferenciado gerado a partir de imagens capturadas por drone. Representa uma vista aerea ortogonal da area de interesse com precisao geometrica.

**Caracteristicas:**
- Formato: GeoTIFF, JPEG2000
- Georeferenciada: coordenadas embarcadas
- Alta resolucao: centimetros por pixel
- Gerada por voo de drone
- Processada pelo backend (reducao de tamanho)

## Bucket

Armazenamento de objetos (S3/MinIO) para arquivos pesados como ortofotos, documentos e midias.

**Estrutura por TENANT:**
```
/{tenant_id}/ortofotos/{ano}/{mes}/
  - original/
  - otimizada/
  - tiles/
/{tenant_id}/documentos/
/{tenant_id}/fotos/
```

## TENANT

Regiao/area de atuacao que define a unidade de segregacao do sistema. Tudo (ortofotos, poligonos, tarefas, agentes) e segregado por TENANT.

**Exemplos de TENANT:**
- Municipio (Prefeitura X)
- Regiao metropolitana
- Assentamento especifico
- Projeto de regularizacao

**Regras:**
- Um usuario pertence a um ou mais TENANTs
- Usuario so enxerga dados do(s) TENANT(s) designado(s)
- Isolamento garantido via RLS no PostgreSQL

## Plugin QGIS (GEOGIS)

Ferramenta instalada no QGIS que permite ao Analista acessar ortofotos, georreferenciar poligonos e publicar trabalho no backend.

**Funcionalidades:**
- Autenticacao dupla (Keycloak + AUTHENTICATION KEY)
- Acesso a ortofotos do TENANT
- Desenho de poligonos (comunidades, quadras, lotes)
- Validacao topologica
- Publicacao no backend

## AUTHENTICATION KEY

Chave adicional de autenticacao exigida pelo Plugin QGIS, alem do login Keycloak. Funciona como uma API key que:
- Habilita/autoriza o uso do plugin
- Vincula a sessao/ambiente ao backend
- Pode ser revogada independentemente do usuario
- Adiciona camada extra de seguranca

**Formato:** String alfanumerica (ex: `carf_key_abc123xyz789`)

## Pacote Temporario

Download unico e temporario disponibilizado ao Agente de Campo contendo:
- Ortofoto (versao para uso offline)
- Poligonos georreferenciados (comunidades/quadras/lotes)
- Metadados necessarios para operacao

**Caracteristicas:**
- Link de download expira apos uso
- Armazenado localmente no dispositivo
- Permite operacao offline completa
