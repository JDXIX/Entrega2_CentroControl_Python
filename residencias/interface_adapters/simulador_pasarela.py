"""Adaptador de entrada: emula la pasarela local, sin hardware."""
from residencias.entities.lectura_sensor import LecturaSensor
from residencias.use_cases.centro_control_residencia import ResultadoRecepcion
from residencias.use_cases.puertos import RecepcionPasarela


class SimuladorPasarela:
    def __init__(self, receptor: RecepcionPasarela) -> None:
        self._receptor = receptor

    def enviar_lectura(self, lectura: LecturaSensor) -> ResultadoRecepcion:
        return self._receptor.recibir_datos(lectura)
