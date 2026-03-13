## DOC-ARQ-01 – Arquitectura de la solución aplicada al ticket FERNANDO-1

### Visión general por capas

- **Capa de presentación**
  - El editor/IDE `Cursor` es la interfaz principal para los desarrolladores.
  - La interacción se realiza mediante:
    - `@.cursor/agents` para agentes especializados (por ejemplo, backend, Jira manager, chatbots).
    - `@.cursor/commands` para flujos de trabajo guiados (por ejemplo, `implement-ticket`, `enrich`).
    - `@.cursor/skills` para conocimiento de dominio y buenas prácticas.

- **Capa de orquestación de agentes (Cursor)**
  - Los agentes combinan skills y reglas del repo para:
    - Leer y enriquecer tickets de Jira.
    - Implementar funcionalidades en el backend.
    - Guiar al usuario en flujos de desarrollo (plan → código → PR).

- **Capa de backend de negocio (repositorio)**
  - Código Python organizado para:
    - Servicios de LangChain (cadenas, agentes, herramientas).
    - Integraciones con APIs externas según vaya creciendo el proyecto.
  - Se siguen las reglas definidas en `.cursor/rules/python.mdc`.

- **Capa de gestión de ciclo de vida (Jira + Git)**
  - Jira (`FERNANDO-*`) como fuente de verdad funcional (requisitos, estados).
  - Git/GitHub como fuente de verdad técnica (código, ramas, PRs).
  - Flujo de estados típico:
    - `To Do` → `In Progress` → `In Review` → `Done`.

### Responsabilidades clave

- Este ticket FERNANDO-1 se centra en:
  - Documentar cómo se conectan estas capas para el resto de tickets del proyecto.
  - Servir de referencia para futuros tickets que utilicen los mismos patrones de arquitectura.

