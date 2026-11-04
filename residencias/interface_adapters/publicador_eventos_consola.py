"""Adaptador de salida: conserva y muestra eventos; NO envía alertas reales."""
from residencias.entities.evento_critico import EventoCritico


class PublicadorEventosConsola:
    def __init__(self) -> None:
        self.eventos_publicados: list[EventoCritico] = []

    def publicar(self, evento: EventoCritico) -> None:
        self.eventos_publicados.append(evento)
        print("\n[DOMAIN EVENT - SIMULACIÓN]")
        print(f"  Tipo: {evento.tipo_evento}")
        print(f"  Origen: {evento.referencia_origen}")
        print("  Publicado en consola; NO se contactó a emergencias.")
