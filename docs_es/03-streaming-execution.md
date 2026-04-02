# Ejecucion en Streaming

> **Resumen en español de la tecnica que permite a Claude Code ejecutar herramientas mientras el LLM sigue respondiendo**

Fuente completa en ingles: [docs/03-streaming-execution.md](../docs/03-streaming-execution.md)

## Idea central

En muchos asistentes, el modelo termina de generar, luego se parsea la llamada a herramienta y recien entonces se ejecuta. Claude Code adelanta ese trabajo y empieza a correr herramientas tan pronto como tiene suficiente informacion.

## Por que cambia la UX

- reduce el tiempo hasta la primera accion visible
- permite superponer pensamiento del modelo con trabajo real
- hace que los workflows con varias herramientas no se vuelvan lineales

En tareas con varias operaciones, esa diferencia puede ser de 2x a 5x en velocidad percibida.

## Componentes clave

### 1. Streaming del modelo

La respuesta del LLM no se espera completa. Se procesa en tiempo real.

### 2. Ejecucion concurrente

Si varias herramientas son seguras y no dependen una de otra, pueden correr al mismo tiempo.

### 3. Manejo parcial de parametros

El sistema puede decidir que ya hay suficiente informacion para empezar, incluso antes de que el mensaje termine por completo.

### 4. Actualizacion progresiva de la UI

El usuario ve progreso, estados intermedios y resultados en vivo.

### 5. Recuperacion ante errores

El loop debe tolerar fallos a mitad del stream sin romper toda la sesion.

## Implicacion tecnica

Esta arquitectura exige coordinacion asincrona fina. No alcanza con "esperar un JSON final". Hay que sincronizar parser, permisos, ejecucion y UI mientras el stream sigue abierto.

## Que conviene leer despues

- [Vision general de la arquitectura](./02-architecture-overview.md)
- [UX de terminal](./06-terminal-ux.md)
- [Ingenieria de produccion](./09-production-engineering.md)
