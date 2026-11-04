"""Pruebas unitarias estándar, sin librerías de terceros."""
import unittest
from contextlib import redirect_stdout
from io import StringIO

from residencias.entities.evaluador_situaciones import EvaluadorSituaciones
from residencias.entities.evento_critico import AlertaDeCaidaDetectada
from residencias.entities.lectura_sensor import LecturaSensor
from residencias.interface_adapters.consulta_residentes_memoria import ConsultaResidentesEnMemoria
from residencias.interface_adapters.publicador_eventos_consola import PublicadorEventosConsola
from residencias.interface_adapters.simulador_pasarela import SimuladorPasarela
from residencias.use_cases.centro_control_residencia import CentroControlResidencia


class PruebasCentroControl(unittest.TestCase):
    def setUp(self) -> None:
        self.publicador = PublicadorEventosConsola()
        self.centro = CentroControlResidencia(
            EvaluadorSituaciones(),
            self.publicador,
            ConsultaResidentesEnMemoria({"DEMO"}),
        )
        self.pasarela = SimuladorPasarela(self.centro)

    def crear_lectura(self, tipo: str, valor, residente: str | None = "DEMO") -> LecturaSensor:
        return LecturaSensor(tipo, valor, "SENSOR-SIMULADO", residente)

    def test_sin_caida_no_genera_evento(self) -> None:
        resultado = self.pasarela.enviar_lectura(self.crear_lectura("caida", False))
        self.assertIsNone(resultado.evento)
        self.assertEqual([], self.publicador.eventos_publicados)

    def test_con_caida_genera_domain_event(self) -> None:
        with redirect_stdout(StringIO()):
            resultado = self.pasarela.enviar_lectura(self.crear_lectura("caida", True))
        self.assertIsInstance(resultado.evento, AlertaDeCaidaDetectada)
        self.assertEqual("AlertaDeCaidaDetectada", resultado.evento.tipo_evento)
        self.assertEqual("SENSOR-SIMULADO", resultado.evento.referencia_origen)
        self.assertEqual(1, len(self.publicador.eventos_publicados))

    def test_movimiento_no_tiene_regla_clinica_inventada(self) -> None:
        resultado = self.pasarela.enviar_lectura(self.crear_lectura("movimiento", "detectado"))
        self.assertIsNone(resultado.evento)

    def test_valor_incorrecto_para_caida_es_rechazado(self) -> None:
        with self.assertRaisesRegex(ValueError, "True o False"):
            self.pasarela.enviar_lectura(self.crear_lectura("caida", "sí"))
        self.assertEqual([], self.publicador.eventos_publicados)

    def test_consulta_de_residente_es_solo_referencia(self) -> None:
        resultado = self.pasarela.enviar_lectura(self.crear_lectura("caida", False, "OTRO"))
        self.assertFalse(resultado.referencia_residente_encontrada)
        self.assertIsNone(resultado.evento)

    def test_lecturas_agregadas_en_memoria(self) -> None:
        self.pasarela.enviar_lectura(self.crear_lectura("caida", False))
        self.pasarela.enviar_lectura(self.crear_lectura("movimiento", "detectado"))
        self.assertEqual(2, len(self.centro.agregar_datos()))

    def test_value_object_es_inmutable(self) -> None:
        from dataclasses import FrozenInstanceError
        lectura = self.crear_lectura("caida", False)
        with self.assertRaises(FrozenInstanceError):
            lectura.valor = True

    def test_evento_es_inmutable(self) -> None:
        from dataclasses import FrozenInstanceError
        evento = AlertaDeCaidaDetectada("SENSOR-SIMULADO")
        with self.assertRaises(FrozenInstanceError):
            evento.tipo_evento = "Otro"


if __name__ == "__main__":
    unittest.main()
