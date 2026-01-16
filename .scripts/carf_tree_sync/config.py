"""Configuracoes do carf_tree_sync."""

from typing import Dict, List

# Nomes de dominios por pasta (numero-slug -> nome legivel)
DOMAIN_NAMES: Dict[str, str] = {
    # Requisitos Funcionais / User Stories
    "01-auth-security": "Autenticacao e Seguranca",
    "02-tenants": "Gestao de Tenants",
    "03-users-teams": "Usuarios e Equipes",
    "04-notifications": "Notificacoes",
    "05-communities": "Gestao de Comunidades",
    "06-units": "Gestao de Unidades",
    "07-holders": "Gestao de Titulares",
    "08-documents-media": "Documentos e Midia",
    "09-layers-features": "Camadas e Features",
    "10-spatial-analysis": "Analise Espacial",
    "11-annotations": "Anotacoes",
    "12-surveys": "Levantamentos Topograficos",
    "13-legitimation": "Processos de Legitimacao",
    "14-offline-sync": "Modo Offline e Sincronizacao",
    "15-data-export": "Exportacao de Dados",
    "16-reports": "Relatorios",
    "17-wms-wmts": "Integracoes WMS/WMTS",
    # Requisitos Nao-Funcionais
    "01-performance": "Performance",
    "02-security": "Seguranca",
    "03-reliability": "Confiabilidade",
    "04-usability": "Usabilidade",
    "05-scalability": "Escalabilidade",
    "06-compatibility": "Compatibilidade",
    "07-maintainability": "Manutenibilidade",
    "08-interoperability": "Interoperabilidade",
}

# Tipos de requisitos com prefixo e titulo
REQUIREMENT_TYPES: Dict[str, Dict[str, str]] = {
    "FUNCTIONAL-REQUIREMENTS": {
        "prefix": "RF",
        "title": "Requisitos Funcionais",
        "singular": "requisito",
        "plural": "requisitos",
    },
    "USER-STORIES": {
        "prefix": "US",
        "title": "User Stories",
        "singular": "user story",
        "plural": "user stories",
    },
    "USE-CASES": {
        "prefix": "UC",
        "title": "Casos de Uso",
        "singular": "caso de uso",
        "plural": "casos de uso",
    },
    "NON-FUNCTIONAL-REQUIREMENTS": {
        "prefix": "RNF",
        "title": "Requisitos Nao-Funcionais",
        "singular": "requisito",
        "plural": "requisitos",
    },
}

# Ordem dos modulos para agrupamento
MODULE_ORDER: List[str] = [
    "GEOWEB",
    "REURBCAD",
    "GEOAPI",
    "GEOGIS",
    "ADMIN",
    "KEYCLOAK",
]

# Pastas a ignorar durante varredura
EXCLUDE_DIRS: List[str] = [
    ".git",
    ".obsidian",
    ".scripts",
    "node_modules",
    ".venv",
    "__pycache__",
    ".claude",
]

# Marcadores de secao gerada
GENERATED_START = "<!-- GENERATED:START - Nao edite abaixo desta linha -->"
GENERATED_END = "<!-- GENERATED:END -->"

# Formato de timestamp
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M"
