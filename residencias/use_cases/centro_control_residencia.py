"""Caso de uso: recepción, agregación, evaluación y publicación de eventos."""
from dataclasses import dataclass
from residencias.entities.evaluador_situaciones import EvaluadorSituaciones
from residencias.entities.evento_critico import EventoCritico
from residencias.entities.lectura_sensor import LecturaSensor
from residencias.use_cases.puertos import ConsultaResidentes, PublicadorEventos


@dataclass(frozen=True)
class ResultadoRecepcion:
    """Resultado del caso de uso para que la UI pueda mostrarlo."""
    lectura: LecturaSensor
    evento: EventoCritico | None
    referencia_residente_encontrada: bool | None


class CentroControlResidencia:
    """Implementa el puerto de entrada RecepcionPasarela (tipado estructural)."""

    def __init__(
        self,
        evaluador: EvaluadorSituaciones,
        publicador: PublicadorEventos,
        consulta_residentes: ConsultaResidentes,
    ) -> None:
        self._evaluador = evaluador
        self._publicador = publicador
        self._consulta_residentes = consulta_residentes
        self._lecturas: list[LecturaSensor] = []

    def recibir_datos(self, lectura: LecturaSensor) -> ResultadoRecepcion:
        """Orquesta un caso de uso sin depender de un protocolo específico."""
        encontrado = None
        if lectura.identificador_residente is not None:
            encontrado = self._consulta_residentes.consultar_referencia(
                lectura.identificador_residente
            )
        evento = self.evaluar_situacion(lectura)
        self._lecturas.append(lectura)
        if evento is not None:
            self.emitir_evento_critico(evento)
        return ResultadoRecepcion(
            lectura=lectura,
            evento=evento,
            referencia_residente_encontrada=encontrado,
        )

    def agregar_datos(self) -> tuple[LecturaSensor, ...]:
        """Consulta el conjunto procesado en memoria, sin base de datos."""
        return tuple(self._lecturas)

    def evaluar_situacion(self, lectura: LecturaSensor) -> EventoCritico | None:
        return self._evaluador.evaluar(lectura)

    def emitir_evento_critico(self, evento: EventoCritico) -> None:
        self._publicador.publicar(evento)
