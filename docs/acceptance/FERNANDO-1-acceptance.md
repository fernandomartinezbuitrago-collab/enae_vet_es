## DOC-AC-01 – Criterios de aceptación (FERNANDO-1)

Para considerar el ticket FERNANDO-1 como **documentación correctamente enriquecida + soporte en el repo**, deben cumplirse al menos estos criterios:

1. **Arquitectura documentada**
   - Existe `docs/architecture/FERNANDO-1-arquitectura.md` que describe:
     - Capas principales (presentación, orquestación de agentes, backend, ciclo de vida Jira+Git).
     - Responsabilidades de cada capa.

2. **Stack tecnológico descrito**
   - Existe `docs/tech-stack/FERNANDO-1-tecnologias.md` donde se detallan:
     - Lenguajes y frameworks principales (Python, LangChain, etc.).
     - Uso de Cursor, Jira y Git.

3. **Flujo de trabajo definido**
   - Existe `docs/workflows/FERNANDO-1-workflow.md` que explica:
     - Cómo se usa Jira + Git + Cursor durante el ciclo de vida de un ticket.
     - En qué puntos se crean ramas, PRs y se cambian estados de Jira.

4. **Índice / Glosario de DOCs en el ticket**
   - El ticket FERNANDO-1 referencia explícitamente estos documentos como:
     - DOC-ARQ-01, DOC-TEC-01, DOC-WF-01, DOC-AC-01, DOC-OOO-01.

5. **Out of scope claro**
   - El ticket FERNANDO-1 lista de forma explícita que:
     - No se modifican las business rules de Cursor.
   - Cualquier otra exclusión relevante queda documentada en DOC-OOO-01.

6. **Definición de Done**
   - Para la fase de documentación, se considera cumplida cuando:
     - Los documentos anteriores existen en el repo (o en Confluence) y están enlazados desde el ticket.
   - Para la fase de implementación futura, se recordará que el Done real incluirá:
     - Código mergeado en `main` y validado por tests/QA, según se describa en nuevos tickets.

