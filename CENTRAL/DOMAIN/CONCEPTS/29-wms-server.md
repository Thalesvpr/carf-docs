---
type: leaf
status: approved
updated: 2026-01-24
---

# Servidor WMS

Servidor de mapas externo que fornece ortofotos e imagens de satelite como camadas de base para visualizacao. Usa protocolo padrao OGC WMS ou WMTS.

Ortofotos de drone e imagens de satelite sao referencia visual essencial para validacao de geometrias. Analistas comparam poligonos desenhados com edificacoes visiveis nas imagens.

## Configuracao

Cadastro inclui URL do servico e credenciais de acesso se necessario. Sistema consulta capacidades do servidor descobrindo camadas disponiveis para uso.

## Tipos de Servico

WMS renderiza imagens dinamicamente a cada requisicao. WMTS serve tiles pre-renderizados, mais rapido para mapas base de alta resolucao.

## Monitoramento

Sistema valida periodicamente conectividade com servidores cadastrados. Detecta problemas automaticamente alertando administradores antes que usuarios encontrem mapas quebrados.

## Uso

Camadas sao exibidas como background em interfaces de mapa. Analistas ajustam poligonos de unidades snapping vertices a footprints de edificacoes visiveis na ortofoto.
