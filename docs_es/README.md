# Claude Code Wiki

> **Indice en español de la documentacion sobre la arquitectura, los patrones y las ventajas tecnicas de Claude Code**

## Que cubre esta seccion

`docs_es/` ofrece una ruta de lectura en español para toda la wiki. Cada pagina resume el tema principal, destaca las ideas mas importantes y enlaza con la version completa en ingles dentro de [`docs/`](../docs/README.md).

Esta seccion esta pensada para:

- entender rapido las ideas clave sin recorrer primero toda la documentacion extensa
- navegar la wiki desde enlaces en español
- identificar que guia en ingles conviene leer a fondo segun el tema

## Navegacion rapida

1. **[Ventajas competitivas](./01-competitive-advantages.md)**  
   Resumen de las 10 innovaciones que diferencian a Claude Code.

2. **[Vision general de la arquitectura](./02-architecture-overview.md)**  
   Panorama del sistema: UI, comandos, herramientas y servicios.

3. **[Ejecucion en streaming](./03-streaming-execution.md)**  
   Como Claude Code ejecuta herramientas mientras el LLM sigue generando.

4. **[Gestion de contexto](./04-context-management.md)**  
   Pipeline de 5 capas para conversaciones largas sin limpieza manual.

5. **[Orquestacion multiagente](./05-multi-agent-orchestration.md)**  
   Tipos de agentes, coordinacion y cache compartida.

6. **[UX de terminal](./06-terminal-ux.md)**  
   Por que React + Ink produce una CLI con experiencia de nivel IDE.

7. **[Modelo de seguridad](./07-security-model.md)**  
   AST, permisos, sandboxing y controles empresariales.

8. **[Ecosistema de integracion](./08-integration-ecosystem.md)**  
   MCP, LSP, plugins, skills y bridge mode.

9. **[Ingenieria de produccion](./09-production-engineering.md)**  
   Telemetria, confiabilidad, arranque rapido y operacion a escala.

10. **[Lecciones aprendidas](./10-lessons-learned.md)**
    Principios de arquitectura y decisiones que valen la pena copiar.

11. **[Vulnerabilidades de seguridad](./12-security-vulnerabilities.md)**
    Análisis integral de seguridad y evaluación de vulnerabilidades.
    Vulnerabilidades Critical/High/Medium con puntajes CVSS.
    Recomendaciones de remediación e infraestructura de seguridad.

## Como usar estas guias

**Si evaluas Claude Code**:
- empieza por [Ventajas competitivas](./01-competitive-advantages.md)
- sigue con [Vision general de la arquitectura](./02-architecture-overview.md)
- revisa [Modelo de seguridad](./07-security-model.md) si te importa el riesgo operativo

**Si construyes herramientas de IA**:
- lee [Ejecucion en streaming](./03-streaming-execution.md)
- continua con [Gestion de contexto](./04-context-management.md)
- termina con [Lecciones aprendidas](./10-lessons-learned.md)

**Si buscas patrones de producto e integracion**:
- revisa [UX de terminal](./06-terminal-ux.md)
- luego [Ecosistema de integracion](./08-integration-ecosystem.md)
- y [Ingenieria de produccion](./09-production-engineering.md)

## Nota sobre el alcance

Estas paginas en español funcionan como resúmenes guiados de la documentacion principal. Para diagramas completos, ejemplos extensos y desarrollo detallado, usa los enlaces a las paginas originales en ingles.

---

**Punto de partida recomendado:** [🔥 Ventajas competitivas](./01-competitive-advantages.md)
