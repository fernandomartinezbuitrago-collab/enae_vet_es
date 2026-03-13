## DOC-TEC-01 – Tecnologías y stack (FERNANDO-1)

### Lenguajes y ecosistema

- **Python 3.x** como lenguaje principal de backend.

### Frameworks y librerías

- **LangChain**
  - Construcción de cadenas, agentes y herramientas.
  - Integración con proveedores de LLM (OpenAI, Anthropic, etc.).
- **Entorno Cursor**
  - Uso de:
    - `@.cursor/agents` para agentes especializados.
    - `@.cursor/commands` para comandos de flujo de trabajo como `implement-ticket` y `enrich`.
    - `@.cursor/skills` para conocimiento de dominio (veterinario, Jira, negocio).
    - `@.cursor/rules/python.mdc` como guía de estilo y buenas prácticas Python.

### Gestión de trabajo y metodología

- **Jira** (proyecto `FERNANDO`) para:
  - Backlog, sprints y estados de tickets.
  - Trazabilidad entre requisitos y código.
- **SCRUM**
  - Refinement, sprint planning, daily, review y retrospective.

### Control de versiones y CI/CD

- **Git** como sistema de control de versiones.
- **GitHub** (u otro remoto) para:
  - Pull Requests y revisiones.
  - Integración con pipelines de CI:
    - Ejecución de tests.
    - Linters/formatters según las reglas del repo.

