"""Registry para auto-registro de validadores."""

from typing import Dict, List, Type, Optional

from .base import BaseValidator, LocalValidator, GlobalValidator


class ValidatorRegistry:
    """Registry para descoberta e instanciação de validadores."""

    _instance: Optional["ValidatorRegistry"] = None

    def __init__(self):
        """Inicializa registry."""
        self._validators: Dict[str, Type[BaseValidator]] = {}
        self._enabled: Dict[str, bool] = {}

    @classmethod
    def instance(cls) -> "ValidatorRegistry":
        """Retorna instância singleton."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset do singleton (para testes)."""
        cls._instance = None

    def register(self, validator_class: Type[BaseValidator]) -> Type[BaseValidator]:
        """
        Registra uma classe de validador. Pode ser usado como decorator.

        Args:
            validator_class: Classe do validador

        Returns:
            A mesma classe (para uso como decorator)
        """
        self._validators[validator_class.name] = validator_class
        self._enabled[validator_class.name] = True
        return validator_class

    def get(self, name: str) -> Optional[Type[BaseValidator]]:
        """
        Busca validador por nome.

        Args:
            name: Nome do validador

        Returns:
            Classe do validador ou None
        """
        return self._validators.get(name)

    def get_all(self) -> List[Type[BaseValidator]]:
        """Retorna todos os validadores registrados."""
        return list(self._validators.values())

    def get_enabled(self) -> List[Type[BaseValidator]]:
        """Retorna todos os validadores habilitados."""
        return [
            v for name, v in self._validators.items()
            if self._enabled.get(name, True)
        ]

    def enable(self, name: str) -> None:
        """Habilita um validador."""
        self._enabled[name] = True

    def disable(self, name: str) -> None:
        """Desabilita um validador."""
        self._enabled[name] = False

    def is_enabled(self, name: str) -> bool:
        """Verifica se validador está habilitado."""
        return self._enabled.get(name, True)

    def get_local_validators(self) -> List[Type[LocalValidator]]:
        """Retorna todos os validadores locais habilitados."""
        return [
            v for v in self.get_enabled()
            if issubclass(v, LocalValidator)
        ]

    def get_global_validators(self) -> List[Type[GlobalValidator]]:
        """Retorna todos os validadores globais habilitados."""
        return [
            v for v in self.get_enabled()
            if issubclass(v, GlobalValidator) and not issubclass(v, LocalValidator)
        ]

    def get_validator_names(self) -> List[str]:
        """Retorna nomes de todos os validadores."""
        return list(self._validators.keys())


def validator(cls: Type[BaseValidator]) -> Type[BaseValidator]:
    """
    Decorator para registrar um validador.

    Args:
        cls: Classe do validador

    Returns:
        A mesma classe
    """
    ValidatorRegistry.instance().register(cls)
    return cls
