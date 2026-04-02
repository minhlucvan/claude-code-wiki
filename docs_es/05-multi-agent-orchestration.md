# Orquestacion Multiagente

> **Resumen en español de como Claude Code divide trabajo complejo entre agentes especializados**

Fuente completa en ingles: [docs/05-multi-agent-orchestration.md](../docs/05-multi-agent-orchestration.md)

## Idea central

Un solo agente generalista sirve para tareas simples, pero se vuelve ineficiente cuando hay que investigar, implementar, comparar y verificar en paralelo. Claude Code resuelve eso con varios agentes especializados coordinados por el sistema principal.

## Elementos clave

### Agentes especializados

Cada tipo de agente esta optimizado para una clase distinta de trabajo. Eso evita cargar siempre el mismo contexto y el mismo conjunto de herramientas para todo.

### Patron de fork

Los agentes derivados nacen desde una base comun. Gracias a eso pueden compartir cache de prompt y reducir fuertemente el costo total.

### Coordinacion

Hay una capa que decide:

- que trabajo conviene delegar
- que tareas pueden avanzar en paralelo
- cuando esperar resultados
- como integrar respuestas sin duplicar trabajo

### Sistema de tareas

No todo ocurre en el hilo principal. Parte del valor viene de poder lanzar trabajo lateral mientras el flujo principal sigue avanzando.

## Beneficios concretos

- mejor paralelismo
- menor costo por agente
- prompts mas enfocados
- mejor division del trabajo

## Riesgos que evita

Sin orquestacion formal, el multiagente puede degradarse rapido:

- trabajo duplicado
- conflictos de contexto
- resultados inconexos
- costo excesivo

Claude Code evita eso con roles y ownership mas claros.

## Que conviene leer despues

- [Gestion de contexto](./04-context-management.md)
- [Ingenieria de produccion](./09-production-engineering.md)
- [Lecciones aprendidas](./10-lessons-learned.md)
