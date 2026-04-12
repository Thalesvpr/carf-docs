"""Validadores modulares para documentação CARF."""

from .base import BaseValidator, LocalValidator, GlobalValidator
from .registry import ValidatorRegistry, validator

# Importa validadores locais para auto-registro
from . import local
from . import global_

__all__ = [
    "BaseValidator",
    "LocalValidator",
    "GlobalValidator",
    "ValidatorRegistry",
    "validator",
]
