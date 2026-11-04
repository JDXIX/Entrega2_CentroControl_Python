"""Objeto de valor inmutable del contexto Monitorización."""
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LecturaSensor:
    """El enunciado aporta tipoDato/valor; los IDs son metadatos del prototipo.

    referencia_origen identifica el sensor simulado para trazar el evento.
    identificador_residente es opcional; no todas las lecturas son personales.
    """
    tipo_dato: str
    valor: Any
    referencia_origen: str
    identificador_residente: str | None = None

    def __post_init__(self) -> None:
        if not self.tipo_dato.strip():
            raise ValueError("El tipo de dato no puede estar vacío.")
        if not self.referencia_origen.strip():
            raise ValueError("La referencia de origen no puede estar vacía.")
