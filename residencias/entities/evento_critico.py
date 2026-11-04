"""Domain Events: representan sucesos ya identificados en Monitorización."""
from dataclasses import dataclass


@dataclass(frozen=True)
class EventoCritico:
    tipo_evento: str
    referencia_origen: str


class AlertaDeCaidaDetectada(EventoCritico):
    """Evento nombrado explícitamente como ejemplo en el enunciado académico."""

    def __init__(self, referencia_origen: str) -> None:
        super().__init__(
            tipo_evento="AlertaDeCaidaDetectada",
            referencia_origen=referencia_origen,
        )
