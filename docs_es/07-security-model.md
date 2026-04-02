# Modelo de Seguridad

> **Resumen en español de la estrategia de defensa en profundidad de Claude Code**

Fuente completa en ingles: [docs/07-security-model.md](../docs/07-security-model.md)

## Idea central

Claude Code asume que ejecutar codigo y comandos desde una IA es riesgoso. Por eso combina varias capas: parsing estructural, permisos, sandboxing y controles de administracion.

## Capas principales

### Parsing Bash a nivel AST

El sistema no se queda con una inspeccion superficial de strings. Entiende la estructura del comando y detecta patrones peligrosos incluso cuando estan disfrazados.

### Sistema de permisos

Permite decidir cuando una accion:

- se aprueba automaticamente
- requiere confirmacion
- queda bloqueada

### Reglas con comodines

Sirven para expresar politicas utiles sin tener que enumerar cada comando de forma manual.

### Sandboxing

Cuando el entorno lo permite, la ejecucion puede aislarse para reducir daño potencial.

### Controles empresariales

Politicas gestionadas y restricciones organizacionales completan la capa operativa.

## Amenazas que aborda

- prompt injection
- comandos destructivos
- exfiltracion de datos
- abuso de herramientas de red o shell

## Por que es importante

Muchos asistentes se quedan en prompts o confirmaciones simples. Claude Code trata la seguridad como parte del diseño del sistema, no como un parche de ultimo momento.

## Que conviene leer despues

- [Vision general de la arquitectura](./02-architecture-overview.md)
- [Ingenieria de produccion](./09-production-engineering.md)
- [Lecciones aprendidas](./10-lessons-learned.md)
