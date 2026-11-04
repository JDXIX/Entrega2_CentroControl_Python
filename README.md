# Entrega 2 — Prototipo del Centro de Control de Residencia

**Asignatura:** Arquitectura de Software  
**Estudiante:** [Completar nombre]  
**Lenguaje:** Python 3.10 o superior  
**Componente implementado:** `CentroControlResidencia`  
**Estilo del sistema completo (Entrega 1):** arquitectura orientada a eventos (EDA)  
**Estilo interno del prototipo (Entrega 2):** Clean Architecture y DDD

## 1. Objetivo y alcance

Implementar **solo uno** de los tres componentes principales del diseño de la Entrega 1:
el Centro de Control Central de la Residencia. Recibe lecturas simuladas de una pasarela
local, las agrega en memoria, las evalúa y publica un **Domain Event** cuando recibe
una indicación explícita de caída.

Las entradas se introducen por un menú de consola. No se emplean sensores, hardware,
bases de datos, mensajes reales ni conexión con emergencias. `SimuladorPasarela`
es solamente un adaptador de entrada: no se implementa el módulo embebido completo.
`PublicadorEventosConsola` es solo un adaptador de salida: no se implementa el
servicio central de gestión de alertas.

## 2. Requisitos

- Python 3.10+ instalado.
- No requiere instalar dependencias externas, ni crear entornos virtuales.

## 3. Cómo ejecutar

Abrir una terminal **en la raíz de este proyecto** y ejecutar:

```bash
python main.py
```

En Windows, si `python` no funciona, intentar:

```powershell
py main.py
```

Seleccionar **1** para una lectura sin caída, **2** para simular una caída,
**3** para una lectura de movimiento, **4** para listar las lecturas, **5** para
listar los eventos generados y **0** para salir.

## 4. Caso demostrativo

Al seleccionar `2`:

1. La consola crea `LecturaSensor(tipo_dato="caida", valor=True)`.
2. El adaptador `SimuladorPasarela` entrega la lectura al puerto `RecepcionPasarela`.
3. `CentroControlResidencia` la agrega en memoria y solicita su evaluación.
4. El servicio de dominio `EvaluadorSituaciones` produce el evento
   `AlertaDeCaidaDetectada`.
5. El caso de uso lo envía al puerto `PublicadorEventos`.
6. El adaptador `PublicadorEventosConsola` registra el evento y lo muestra.

Este flujo demuestra comunicación por eventos en el **límite del componente**, sin
pretender que existe un broker, microservicios, red real o una entrega fiable garantizada.

## 5. Clean Architecture: carpetas y reglas de dependencia

```text
Entrega2_CentroControl_Python/
├── main.py                           Inicio de la aplicación
├── residencias/
│   ├── entities/                    Entidades/objetos de valor y servicio de dominio
│   │   ├── lectura_sensor.py        LecturaSensor (Value Object)
│   │   ├── evento_critico.py        EventoCritico y AlertaDeCaidaDetectada
│   │   └── evaluador_situaciones.py EvaluadorSituaciones (Domain Service)
│   ├── use_cases/                   Casos de uso y puertos
│   │   ├── centro_control_residencia.py
│   │   └── puertos.py              RecepcionPasarela, PublicadorEventos, ConsultaResidentes
│   ├── interface_adapters/          Adaptadores de entrada/salida
│   │   ├── simulador_pasarela.py
│   │   ├── publicador_eventos_consola.py
│   │   └── consulta_residentes_memoria.py
│   └── frameworks/                 Interfaz por consola y composición
│       └── consola.py
├── tests/                            Pruebas unitarias
└── diagramas/                        Mermaid: componentes, clases y secuencia
```

**Dependencias hacia el interior:** `Frameworks` conoce los adaptadores y casos de uso;
`Interface Adapters` conoce los puertos de `Use Cases` y los modelos de `Entities`;
`Use Cases` conoce `Entities` y **no** las implementaciones externas;
`Entities` no conoce ninguna dependencia tecnológica del prototipo.

## 6. DDD y consistencia con la Entrega 1

- **Bounded Context Monitorización:** es el ámbito funcional del centro de control:
  `LecturaSensor`, `EvaluadorSituaciones` y `CentroControlResidencia`.
- **Bounded Context Residentes:** solo se consulta una referencia a través del puerto
  `ConsultaResidentes`; en el prototipo lo resuelve un adaptador en memoria.
- **Bounded Context Alertas:** no está implementado; recibiría el `EventoCritico` en
  una solución real. Aquí se simula la publicación en consola.
- **Lenguaje ubicuo:** `LecturaSensor`, `EventoCritico`, `EvaluadorSituaciones`,
  `CentroControlResidencia`, `ConsultaResidentes`, `PublicadorEventos`.
- **Value Object:** `LecturaSensor`, inmutable mediante `@dataclass(frozen=True)`.
- **Domain Event:** `AlertaDeCaidaDetectada`, inmutable, subtipo de `EventoCritico`.
- **Domain Service:** `EvaluadorSituaciones`, sin acceso a archivos o consola.
- **Aggregate:** los agregados candidatos definidos en Entrega 1 (Residente,
  DispositivoEmbebido y Alerta) **no se implementan íntegros**, porque este prototipo
  implementa el centro de control, no esos tres componentes. El evento no modifica
  estado dentro de otro agregado. No se inventan invariantes transaccionales.

En los diagramas originales se usan métodos `recibirDatos`, `agregarDatos`,
`evaluarSituacion`, `emitirEventoCritico` y aquí se implementan sus equivalentes
idiomáticos en Python: `recibir_datos`, `agregar_datos`, `evaluar_situacion`,
`emitir_evento_critico`. Además, el evento incluye `referencia_origen`, campo
reflejado en el diagrama de alertas de la Entrega 1 y útil para rastrear su origen.

## 7. Regla simulada, límites y supuestos

El **único criterio implementado** es: una lectura de tipo `caida` cuyo valor
booleano es `True` produce `AlertaDeCaidaDetectada`. `False` no produce evento.
Otros tipos se reciben y almacenan, pero **no** tienen detección de anomalías.
Esta regla es una decisión demostrativa derivada del ejemplo de caída del enunciado.
No se introducen umbrales de pulsaciones, temperatura, ausencia de movimiento,
frecuencia de muestreo ni latencias garantizadas.

`SENSOR-DEMO` y `RESIDENTE-DEMO` son **etiquetas ficticias exclusivamente
técnicas de simulación**: no representan dispositivos, usuarios ni cantidades
reales. La consulta de identificador no condiciona la emisión de una caída:
funciona como demostración de un puerto hacia el contexto Residentes.

La memoria y la consola **no ofrecen** persistencia, alta disponibilidad,
seguridad clínica, procesamiento en tiempo real, notificación real ni
fiabilidad de entrega; estas son decisiones fuera del prototipo de un componente.

**Datos del caso sin fijar:** número de residencias, dispositivos por residencia,
concurrencia, protocolos/middleware, volumen de mensajes, tamaño de mensajes,
latencia máxima y frecuencia de muestreo. La nota común de la consigna los
requiere para una solución completa; no se atribuyen valores inventados al docente.

## 8. Pruebas

Ejecutar en la raíz:

```bash
python -m unittest discover -s tests -v
```

Las pruebas comprueban recepción normal, detección de caída, evento de dominio,
publicación, referencia de residente, agregación, errores de tipo y la inmutabilidad
del Value Object y del Domain Event.

## 9. Diagramas

Abrir los archivos `.mmd` de `diagramas/` en TryMermaid o Mermaid Live:

- `01_componentes_prototipo.mmd` — organización del componente y sus dependencias.
- `02_clases_prototipo.mmd` — relación de clases y puertos implementados.
- `03_secuencia_prototipo.mmd` — recorrido de una caída simulada.

## 10. Publicar en GitHub

Desde la raíz del proyecto, tras crear un repositorio vacío en GitHub:

```bash
git init
git add .
git commit -m "Entrega 2: centro de control con Clean Architecture"
git branch -M main
git remote add origin URL_DEL_REPOSITORIO
git push -u origin main
```

Sustituir `URL_DEL_REPOSITORIO` por la URL real del repositorio creado.

## 11. Mini-guion para la defensa

«Implementé únicamente el Centro de Control de Residencia, uno de los tres
componentes de la Entrega 1. La entrada viene de una pasarela simulada,
no de un sensor físico. El caso de uso recibe y agrega lecturas, pide a un
servicio de dominio que las evalúe y, si la lectura indica una caída,
publica el Domain Event AlertaDeCaidaDetectada. La publicación se adapta
a consola mediante un puerto. Así, la lógica no depende de infraestructura.
Mantengo los límites de Monitorización, Residentes y Alertas. No incluyo
umbrales clínicos ni protocolos reales que no se definieron en el enunciado».
