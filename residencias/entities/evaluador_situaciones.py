"""Servicio de dominio: identifica situaciones relevantes a partir de lecturas."""
from residencias.entities.evento_critico import (
    AlertaDeCaidaDetectada,
    EventoCritico,
)
from residencias.entities.lectura_sensor import LecturaSensor


class EvaluadorSituaciones:
    def evaluar(self, lectura: LecturaSensor) -> EventoCritico | None:
        """Detecta solo una caída explícita (True), SIN umbrales clínicos.

        Cualquier otro tipo de lectura se conserva, pero no se evalúa
        clínicamente porque el PDF no define límites numéricos.
        """
        if lectura.tipo_dato.lower() == "caida":
            if type(lectura.valor) is not bool:
                raise ValueError(
                    "Una lectura de caída simulada debe ser True o False."
                )
            if lectura.valor is True:
                return AlertaDeCaidaDetectada(lectura.referencia_origen)
        return None
