"""Puertos abstractos: no dependen de consola, red ni persistencia."""
from typing import Protocol
from residencias.entities.evento_critico import EventoCritico
from residencias.entities.lectura_sensor import LecturaSensor


class PublicadorEventos(Protocol):
    def publicar(self, evento: EventoCritico) -> None: ...


class ConsultaResidentes(Protocol):
    def consultar_referencia(self, identificador: str) -> bool: ...


class RecepcionPasarela(Protocol):
    def recibir_datos(self, lectura: LecturaSensor) -> "ResultadoRecepcion": ...


# Se utiliza una referencia diferida para evitar importar el caso de uso
# en el propio contrato de entrada. El tipo se resolverá por anotación.
if False:  # pragma: no cover (solo para tipado estático)
    from residencias.use_cases.centro_control_residencia import ResultadoRecepcion
