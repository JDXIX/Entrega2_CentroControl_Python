"""Adaptador simulado del BC Residentes: no accede a datos reales."""


class ConsultaResidentesEnMemoria:
    def __init__(self, identificadores: set[str]) -> None:
        self._identificadores = set(identificadores)

    def consultar_referencia(self, identificador: str) -> bool:
        return identificador in self._identificadores
