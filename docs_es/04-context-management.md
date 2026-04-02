# Gestion de Contexto

> **Resumen en español del sistema de 5 capas que permite conversaciones largas sin perder continuidad**

Fuente completa en ingles: [docs/04-context-management.md](../docs/04-context-management.md)

## Idea central

Claude Code trata el contexto como un recurso que se administra continuamente. En vez de esperar a que se rompa la ventana de contexto, compacta y reorganiza el historial de forma automatica.

## El problema que resuelve

Los asistentes convencionales suelen caer en alguno de estos modelos:

- truncar mensajes antiguos
- pedir al usuario limpiar manualmente
- perder continuidad al iniciar una sesion nueva

Claude Code reemplaza eso con una canalizacion progresiva.

## Las 5 capas, en sentido practico

1. **Mensajes recientes intactos**  
   Lo mas cercano a la conversacion actual se conserva con maxima fidelidad.

2. **Historial intermedio resumido**  
   El contexto menos inmediato se compacta sin eliminarlo del todo.

3. **Memoria estructurada**  
   Ciertos hechos o decisiones persisten de forma mas estable.

4. **Optimización de cache**  
   La compactacion intenta no desperdiciar tokens ni recomputar mas de lo necesario.

5. **Control de presupuesto de tokens**  
   El sistema fuerza que la sesion siga entrando dentro del limite util.

## Por que importa

- evita interrupciones al usuario
- preserva continuidad en sesiones largas
- reduce mucho el costo de conversaciones extensas
- hace mas predecible el comportamiento del asistente

## Tradeoff principal

Toda compactacion implica resumir. La dificultad real no es resumir, sino hacerlo sin degradar decisiones, restricciones o contexto tecnico critico. Esa es una de las piezas mas valiosas del sistema.

## Que conviene leer despues

- [Ejecucion en streaming](./03-streaming-execution.md)
- [Orquestacion multiagente](./05-multi-agent-orchestration.md)
- [Lecciones aprendidas](./10-lessons-learned.md)
