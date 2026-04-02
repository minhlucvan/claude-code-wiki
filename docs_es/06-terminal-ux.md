# UX de Terminal

> **Resumen en español de por que Claude Code usa React + Ink para construir una CLI rica y operable**

Fuente completa en ingles: [docs/06-terminal-ux.md](../docs/06-terminal-ux.md)

## Idea central

Claude Code trata la terminal como una interfaz de producto, no como una simple salida de texto. Por eso usa componentes, estado y renderizado incremental.

## Que aporta React + Ink

- composicion de interfaz por componentes
- actualizaciones de estado predecibles
- renderizado dinamico para progreso y resultados
- posibilidad de construir interacciones mas ricas sin abandonar la CLI

## Capacidades visibles

- progreso en tiempo real
- spinners y estados intermedios
- renderizado de diffs
- paleta de comandos
- modo Vim y navegacion por teclado

## Por que esto importa

En una herramienta de IA, gran parte de la confianza del usuario depende de ver que esta pasando. Una UX pobre vuelve opaco el sistema, aunque internamente sea potente.

Con una UI mas rica:

- baja la ansiedad durante tareas largas
- mejora la inspeccion de cambios
- aumenta la capacidad de correccion antes de ejecutar acciones

## Valor arquitectonico

La decision de usar React en terminal no es solo estetica. Tambien ordena el codigo y facilita manejar estados complejos en sesiones largas.

## Que conviene leer despues

- [Ejecucion en streaming](./03-streaming-execution.md)
- [Modelo de seguridad](./07-security-model.md)
- [Ecosistema de integracion](./08-integration-ecosystem.md)
