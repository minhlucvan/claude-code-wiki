# Vision General de la Arquitectura

> **Resumen en español de como Claude Code organiza su sistema para operar como herramienta de IA de nivel produccion**

Fuente completa en ingles: [docs/02-architecture-overview.md](../docs/02-architecture-overview.md)

## Idea central

Claude Code separa bien sus capas: interfaz, comandos, herramientas, motor de consulta y servicios auxiliares. Esa division hace posible iterar rapido sin convertir el sistema en un bloque monolitico dificil de mantener.

## Capas principales

### UI de terminal

La experiencia visible al usuario esta montada con React + Ink. Esa capa maneja:

- mensajes y respuestas
- progreso de herramientas
- barras, paneles y estados transitorios
- interaccion mediante teclado y paleta de comandos

### Capa de comandos

Los slash commands encapsulan workflows frecuentes como revisar codigo, hacer commits o administrar contexto. Sirven como interfaz de alto nivel encima del motor principal.

### Query engine

Es el nucleo operativo. Coordina:

- llamadas al LLM
- streaming de respuestas
- ejecucion de herramientas
- control de contexto
- seguimiento de costo y tokens

### Herramientas

Claude Code dispone de muchas herramientas autocontenidas con contratos consistentes. Esto simplifica permisos, trazabilidad y composicion.

### Servicios de soporte

Incluyen telemetria, configuracion, politicas, integraciones y otras piezas transversales necesarias para operar en produccion.

## Por que esta estructura funciona

- separa responsabilidades con claridad
- hace posible probar subsistemas por separado
- permite añadir integraciones sin romper el nucleo
- reduce el acoplamiento entre UX, LLM y herramientas

## Lo mas destacable

La arquitectura esta diseñada para loops iterativos entre modelo y herramientas, no para un flujo simple de "pregunta, respuesta". Eso la hace mucho mas adecuada para tareas reales de ingenieria.

## Que conviene leer despues

- [Ejecucion en streaming](./03-streaming-execution.md)
- [Orquestacion multiagente](./05-multi-agent-orchestration.md)
- [Ingenieria de produccion](./09-production-engineering.md)
