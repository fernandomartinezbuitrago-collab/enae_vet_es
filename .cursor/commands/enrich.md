# Command: Enrich (Enriquecer ticket Jira)

**Descripción:** Usa este comando cuando un **Project Manager** necesite **enriquecer un ticket existente de Jira**. El objetivo es leer el ticket, encontrar vacíos de información, hacer las preguntas mínimas necesarias y **actualizar la descripción del ticket** (no comentarios) para que siempre incluya arquitectura, tecnologías, flujo de trabajo, glosario de documentación, out of scope, snippets de código (si aplica) y criterios de aceptación que referencien estas secciones.

> **Subagente recomendado:** `@.cursor/agents/veterinary-jira-ticket-manager.mdc`  
> **Skills recomendadas:**  
> - Negocio (si aplica esterilización): `@.cursor/skills/veterinary-sterilization-business-expert/SKILL.md`  
> - Estructura Jira: `@.cursor/skills/jira-best-practices-expert/SKILL.md`

---

## Fase 1 – Leer y entender el ticket

- El Project Manager (y el agente) debe:
  - Leer el ticket actual en Jira (resumen, descripción, estado, enlaces).
  - Identificar:
    - Objetivo del ticket.
    - Alcance funcional/técnico aparente.
    - Dependencias conocidas (epic, otros tickets, documentos).
  - Reformular en 2–4 frases qué intenta conseguir el ticket, en lenguaje de negocio.

---

## Fase 2 – Detectar vacíos y coherencia

- Revisar la descripción actual y localizar:
  - Ausencia de arquitectura o tecnologías explícitas.
  - Falta de definición del flujo de trabajo afectado.
  - Ausencia de índice/glosario de documentación (DOCs).
  - Falta de sección clara de “Out of scope” (especialmente: **no modificar business rules de Cursor**).
  - Falta de snippets de código de referencia cuando ayuden a entender el impacto técnico.
  - CAC poco claros o inexistentes.
- Hacer una lista breve de **gaps** que se van a cubrir con el enriquecimiento.

---

## Fase 3 – Preguntas y aclaraciones (solo si son necesarias)

- Si la información del ticket y del contexto no es suficiente:
  - Formular **preguntas concretas y mínimas** al stakeholder (PO, negocio, tech lead).
  - Ejemplos:
    - ¿Qué partes de la arquitectura se ven afectadas (módulos, servicios, integraciones)?
    - ¿Qué tecnologías están decididas y cuáles están abiertas?
    - ¿Qué flujo de trabajo de usuario/operación se quiere cambiar o crear?
    - ¿Qué documentación existe ya y dónde vive (repo, Confluence, drive…)?
  - Mientras llegan respuestas, se pueden ir preparando secciones genéricas (plantillas) para arquitectura, tecnologías, flujo y DOCs que luego se concretan.

---

## Fase 4 – Enriquecer la **descripción principal** del ticket (no comentarios)

Actualizar la **descripción general** del ticket (campo Description) para que, como mínimo, incluya estas secciones, en este orden aproximado:

1. **Arquitectura**
   - Describir la arquitectura relevante para este ticket:
     - Capas implicadas (por ejemplo: frontend/IDE Cursor, capa de agentes/comandos, backend, integraciones externas).
     - Componentes clave que se verán afectados.
     - Relaciones importantes (quién llama a quién, datos principales que fluyen).
   - Mantenerlo al nivel necesario para que cualquier dev del equipo entienda el contexto.

2. **Tecnologías**
   - Enumerar las tecnologías concretas que se usarán:
     - Lenguajes (p. ej. Python).
     - Frameworks/bibliotecas (p. ej. LangChain, librerías de testing, etc.).
     - Infraestructura o servicios externos relevantes.
   - Aclarar si alguna tecnología está por decidir (y bajo qué criterios).

3. **Flujo de trabajo**
   - Definir el **workflow** que este ticket afecta o introduce:
     - Nivel usuario/negocio (qué hace la persona, en qué orden).
     - Nivel sistema (qué módulos o servicios participan, en qué secuencia).
   - Cuando aplique, alinear con el flujo de estados en Jira (To Do → In Progress → In Review → Done).

4. **Índice / Glosario de documentación (DOCs)**
   - Añadir un pequeño glosario con todos los documentos relevantes para este ticket:
     - Identificador/nombre del documento (p. ej. DOC-ARQ-01, DOC-TEC-01…).
     - Descripción corta del contenido.
     - Ubicación o enlace (repo, Confluence, etc.) si ya existe o indicación de que será creado en otro ticket.

5. **Out of scope**
   - Incluir explícitamente una sección de **Fuera de alcance (Out of scope)** que siempre contenga:
     - “**Out of scope: Modificar business rules de Cursor**”.
   - Añadir otros elementos que se excluyan deliberadamente de este ticket para evitar ambigüedad.

6. **Snippets de código (si aplica)**
   - Si el ticket tiene impacto claramente técnico:
     - Incluir uno o varios **snippets de código de ejemplo** (en la descripción), que ilustren:
       - Puntos de extensión previstos.
       - Interfaces esperadas.
       - Ejemplos de uso relevantes.
   - Los snippets deben ser ilustrativos, no una implementación completa.

7. **Acceptance Criteria (CAC)**
   - Definir criterios de aceptación que referencien explícitamente las secciones anteriores (1–6):
     - Ejemplos:
       - “La sección de Arquitectura describe claramente capas y componentes afectados.”
       - “La sección de Tecnologías lista todas las tecnologías clave que se usarán en la implementación.”
       - “El Flujo de trabajo está definido para usuario y sistema.”
       - “El Índice/Glosario de DOCs incluye todos los documentos necesarios, con descripción y ubicación.”
       - “La sección Out of scope incluye, como mínimo, que NO se modifican las business rules de Cursor.”
       - “Si procede, hay snippets de código que ayuden a entender el impacto técnico.”
   - Los CAC deben ser **testables** en una demo o revisión de ticket: alguien puede ir sección por sección y validar si está presente y correcta.

> **Importante:** Todo este enriquecimiento debe ir en la **descripción principal del ticket**, no como comentarios separados. Los comentarios pueden usarse solo para explicar por qué se hicieron ciertos cambios, si es necesario.

---

## Fase 5 – Guardar cambios y confirmar consistencia

- Antes de dar por terminado el enriquecimiento:
  - Revisar que **todas las secciones (1–7)** están presentes y razonablemente completas.
  - Verificar que los CAC reflejan que esas secciones existen y son revisables.
  - Si se han tomado decisiones o introducido supuestos importantes, mencionarlos brevemente en una sub-sección de “Notas” dentro de la descripción (opcional).
- Si el agente puede editar el ticket vía integración Jira:
  - Aplicar los cambios directamente en el campo de descripción.
- Si no tiene acceso:
  - Generar una versión final de la descripción para que el Project Manager la copie y pegue en Jira.

Deja siempre el ticket en un estado en el que cualquier miembro del equipo pueda entender el **qué**, el **por qué** y el **cómo a alto nivel** con solo leer la descripción.

