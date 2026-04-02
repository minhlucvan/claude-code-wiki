# Ecosistema de Integracion

> **Resumen en español de como Claude Code se conecta con herramientas, IDEs y sistemas externos**

Fuente completa en ingles: [docs/08-integration-ecosystem.md](../docs/08-integration-ecosystem.md)

## Idea central

Claude Code no funciona como un entorno cerrado. Su arquitectura permite tanto consumir capacidades externas como integrarse dentro de otros flujos de trabajo.

## Piezas principales

### MCP en doble rol

Claude Code puede:

- usar servidores MCP externos para ampliar sus herramientas
- exponer sus propias capacidades para que otros clientes las consuman

Esa dualidad le da mucha flexibilidad.

### LSP

La integracion con protocolos de lenguaje mejora analisis, navegacion y capacidades sensibles al codigo.

### OAuth e identidad

La autenticacion con cuenta y permisos forma parte del producto real, no de una demo aislada.

### Plugins y skills

El sistema admite extensiones mas ligeras y personalizables que permiten adaptar comportamiento y herramientas segun el entorno.

### Bridge mode

Hace posible la comunicacion bidireccional con IDEs y otras interfaces.

## Por que esto importa

- evita un ecosistema cerrado
- facilita componer workflows con herramientas existentes
- reduce el costo de añadir nuevas capacidades
- mejora la adopcion en equipos con flujos mixtos CLI + IDE

## Que conviene leer despues

- [UX de terminal](./06-terminal-ux.md)
- [Ingenieria de produccion](./09-production-engineering.md)
- [Ventajas competitivas](./01-competitive-advantages.md)
