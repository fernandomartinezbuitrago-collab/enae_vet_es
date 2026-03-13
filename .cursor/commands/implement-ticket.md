# Command: Implementar ticket con CAC (veterinary-langchain-backend)

**Descripción:** Usa este comando cuando quieras que el agente `veterinary-langchain-backend` implemente un ticket cuya definición incluye CAC (Criterios de Aceptación y/o Checklist). El agente debe seguir **todas** las fases siguientes, de forma secuencial y completa.

> **Agente responsable:** `@.cursor/agents/veterinary-langchain-backend.mdc`

---

## Fase 1 – Leer el ticket

- **Entrada esperada del usuario:**
  - Enlace o ID del ticket (Jira, GitHub Issue, Linear, etc.) **y/o**
  - Texto pegado con:
    - Título y descripción.
    - CAC (criterios de aceptación) y tareas checklist asociadas.
    - Información de módulo/servicio afectado, si existe.
- **Acciones del agente:**
  - Extraer:
    - Título y resumen funcional.
    - Lista de CAC (cada ítem como punto separado).
    - Alcance técnico (servicios, módulos, endpoints, modelos de datos).
  - Reformular el ticket en tus propias palabras (2–4 frases).
  - Señalar claramente cualquier **no-objetivo** que se infiera (cosas que NO se deben tocar).

---

## Fase 2 – Crear el plan

- **Objetivo:** Transformar el CAC en un plan técnico accionable.
- **Acciones del agente:**
  - Proponer un plan de implementación corto (3–7 pasos) que incluya:
    - Archivos/módulos a tocar.
    - Cambios de datos/API si los hubiera.
    - Tests a crear o actualizar.
  - Mapear **cada ítem del CAC** al menos a un paso concreto del plan (indicarlo explícitamente).
  - Declarar los supuestos relevantes que estás haciendo.

---

## Fase 3 – Hacer las preguntas apropiadas (solo si son necesarias)

- Si falta información crítica (reglas de negocio, contratos de API, restricciones de entorno, prioridades), el agente:
  - Formula **preguntas específicas y mínimas** al usuario.
  - Mientras espera respuestas, avanza en trabajo seguro y desacoplado:
    - Refactors internos.
    - Estructura de tests.
    - Documentación técnica no dependiente de las decisiones abiertas.

---

## Fase 4 – Desarrollar el código

- El agente debe:
  - Seguir el plan y actualizarlo si aprende nueva información.
  - Trabajar en pasos pequeños:
    - Abrir archivos relevantes.
    - Aplicar cambios enfocados y consistentes con las reglas Python del repo.
  - Implementar la lógica necesaria para cumplir **todos los CAC**:
    - Código Python + LangChain siguiendo las prácticas de `veterinary-langchain-backend`.
    - Añadir o modificar tests para cubrir:
      - Caso feliz principal por cada CAC.
      - Al menos un caso de error o borde relevante.
  - Ejecutar tests/linters disponibles y corregir errores que se introduzcan.

---

## Fase 5 – Mover el ticket de “To Do” a “In Progress”

- En cuanto se inicia la implementación real:
  - **Si el agente tiene acceso al sistema de tickets:**
    - Actualizar el estado del ticket de **To Do** a **In Progress**.
    - Añadir una nota corta (1 frase) indicando que el desarrollo ha comenzado y se sigue este comando.
  - **Si el agente NO tiene acceso:**
    - Indicar al usuario que mueva el ticket a **In Progress**.
    - Proporcionar una frase lista para copiar/pegar con el status actual.

---

## Fase 6 – Crear la Pull Request con buena descripción

- El agente crea una rama que contenga el número de ticket y despues crea un pull request against main
  - Referencia al ticket (ID y/o URL).
  - **Resumen funcional** en 2–4 viñetas, centrado en:
    - Cambios de comportamiento.
    - Impacto para usuarios o sistemas.
  - **Detalles de implementación** relevantes:
    - Cambios en APIs, modelos, migraciones o performance.
    - Riesgos, trade-offs y compatibilidad hacia atrás.
  - **Test Plan** claro:
    - Qué pruebas se han ejecutado (unitarias, integración, manuales).
    - Comandos o pasos concretos para reproducirlas.
  - Explicitar cualquier CAC que **no** quede cubierto todavía (con justificación y, si aplica, propuesta de follow-up).

---

## Fase 7 – Mover el ticket de “In Progress” a “In Review”

- Una vez abierta la PR:
  - **Si hay integración con el sistema de tickets:**
    - Actualizar el estado del ticket a **In Review**.
    - Asociar/enlazar la PR al ticket.
  - **Si NO hay integración:**
    - Pedir al usuario que mueva el ticket a **In Review**.
    - Proporcionar:
      - Enlace de la PR.
      - Un resumen corto (1–2 frases) para pegar en el ticket.
- El agente debe dejar claramente indicados:
  - Riesgos conocidos o puntos delicados.
  - Trabajo pendiente o tickets de seguimiento recomendados (si los hay).

