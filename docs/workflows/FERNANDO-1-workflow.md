## DOC-WF-01 – Flujo de trabajo SCRUM + Jira + Git + Cursor (FERNANDO-1)

### Flujo a nivel de Jira + Git + Cursor

1. **Refinement del ticket**
   - El Product Owner define:
     - Contexto de negocio.
     - Alcance funcional.
     - Criterios de aceptación (CAC).
   - El equipo técnico valida la viabilidad.

2. **Planificación de sprint**
   - Se estima el ticket (story points).
   - Se decide si entra en el próximo sprint.
   - Se bosqueja una estrategia técnica inicial.

3. **Inicio de desarrollo – estado Jira: `In Progress`**
   - Se crea una rama de Git (por ejemplo, `feature/FERNANDO-1-readme-improvements`).
   - En Cursor se usa el comando `implement-ticket` con el enlace del ticket.
   - El agente backend genera un plan y empieza con cambios pequeños.

4. **Desarrollo iterativo**
   - Cambios incrementales en el código y/o documentación.
   - Se usan comandos como `enrich` para mantener los tickets bien documentados.
   - Se ejecutan tests y linters conforme se va avanzando.

5. **Pull Request – estado Jira: `In Review`**
   - Se abre una PR que referencia `FERNANDO-1`.
   - La PR incluye:
     - Resumen funcional.
     - Detalles técnicos relevantes.
     - Test plan ejecutado.
   - Revisores validan el cambio y los CAC.

6. **Merge y cierre – estado Jira: `Done`**
   - Se hace merge de la rama a `main`.
   - El pipeline de CI pasa en verde.
   - Se verifica que los criterios de aceptación estén cumplidos.
   - El ticket Jira se mueve a `Done` y queda enlazado con la PR.

