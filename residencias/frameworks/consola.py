"""Capa externa: interfaz de consola y composición de dependencias."""
from residencias.entities.evaluador_situaciones import EvaluadorSituaciones
from residencias.entities.lectura_sensor import LecturaSensor
from residencias.interface_adapters.consulta_residentes_memoria import (
    ConsultaResidentesEnMemoria,
)
from residencias.interface_adapters.publicador_eventos_consola import (
    PublicadorEventosConsola,
)
from residencias.interface_adapters.simulador_pasarela import SimuladorPasarela
from residencias.use_cases.centro_control_residencia import CentroControlResidencia

# Identificadores ficticios y exclusivos para demostración.
RESIDENTE_DEMO = "RESIDENTE-DEMO"
SENSOR_DEMO = "SENSOR-DEMO"


def ejecutar_consola() -> None:
    """Permite simular lecturas por teclado (sin frecuencias predefinidas)."""
    publicador = PublicadorEventosConsola()
    consulta = ConsultaResidentesEnMemoria({RESIDENTE_DEMO})
    centro = CentroControlResidencia(EvaluadorSituaciones(), publicador, consulta)
    pasarela = SimuladorPasarela(centro)

    while True:
        print("\n" + "=" * 52)
        print("CENTRO DE CONTROL DE RESIDENCIA | PROTOTIPO")
        print("=" * 52)
        print("1. Simular lectura SIN caída")
        print("2. Simular lectura CON caída")
        print("3. Simular lectura de movimiento")
        print("4. Ver lecturas procesadas")
        print("5. Ver eventos publicados")
        print("0. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            print("Fin de la simulación.")
            break
        if opcion in ("1", "2", "3"):
            if opcion == "3":
                lectura = LecturaSensor(
                    tipo_dato="movimiento",
                    valor="detectado",  # ejemplo simulado, no regla médica
                    referencia_origen=SENSOR_DEMO,
                    identificador_residente=RESIDENTE_DEMO,
                )
            else:
                lectura = LecturaSensor(
                    tipo_dato="caida",
                    valor=(opcion == "2"),
                    referencia_origen=SENSOR_DEMO,
                    identificador_residente=RESIDENTE_DEMO,
                )
            resultado = pasarela.enviar_lectura(lectura)
            print(f"\n[LECTURA] {lectura.tipo_dato} = {lectura.valor}")
            print(f"[REFERENCIA RESIDENTE - SIMULADA] Encontrada: "
                  f"{resultado.referencia_residente_encontrada}")
            if resultado.evento is None:
                print("[RESULTADO] Sin evento crítico identificado "
                      "por la regla demostrativa.")
            else:
                print("[RESULTADO] Evento crítico entregado al publicador.")
        elif opcion == "4":
            lecturas = centro.agregar_datos()
            print(f"\nLecturas almacenadas en memoria: {len(lecturas)}")
            for indice, lectura in enumerate(lecturas, 1):
                print(f"  {indice}. {lectura.tipo_dato} = {lectura.valor} "
                      f"(origen: {lectura.referencia_origen})")
        elif opcion == "5":
            print(f"\nEventos registrados en memoria: "
                  f"{len(publicador.eventos_publicados)}")
            for indice, evento in enumerate(publicador.eventos_publicados, 1):
                print(f"  {indice}. {evento.tipo_evento} "
                      f"(origen: {evento.referencia_origen})")
        else:
            print("Opción no válida. Intente nuevamente.")
