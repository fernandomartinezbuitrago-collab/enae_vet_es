# Chatbot Clinica Veterinaria - MVP Esterilizacion

Repositorio del MVP para asistir en dudas preoperatorias y soporte operativo de esterilizacion/castracion en clinica veterinaria.

## Vision del producto (MVP)

- Reducir la carga administrativa del equipo con respuestas guiadas y consistentes.
- Estandarizar la informacion preoperatoria para tutores de mascotas.
- Preparar la base para integracion de agenda y validacion de disponibilidad.

## Miembros del equipo

- Product Manager: TBD
- Backend: TBD
- Frontend: TBD
- QA/Soporte: TBD

## Enlaces del proyecto

- Jira (proyecto): [FERNANDO - Enae-vet-es](https://fernandomartinezbuitrago.atlassian.net/jira/software/projects/FERNANDO/summary)
- Ticket activo README maestro: [FERNANDO-14](https://fernandomartinezbuitrago.atlassian.net/browse/FERNANDO-14)
- Vercel (deploy): TBD
- URL publica del chatbot: TBD

## Estructura esperada del repositorio

La estructura tecnica aun esta en evolucion. Como guia base:

- `README.MD`: documento maestro del proyecto.
- `.cursor/docs/Tickets.md`: backlog de referencia para epics y tickets.
- `.cursor/commands/`: comandos operativos del flujo del equipo.
- `.cursor/skills/`: skills de soporte para PM y desarrollo.

## Instalacion local (base)

> Nota: si cambian los comandos reales del proyecto, actualiza esta seccion en el mismo ticket o en un ticket de mantenimiento documental.

1. Clona el repositorio.
2. Crea y activa entorno virtual.
3. Instala dependencias del proyecto.
4. Configura variables de entorno.
5. Arranca la aplicacion en modo local.

Ejemplo de comandos (ajustar si aplica):

```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Variables de entorno

Crear archivo `.env` local (no subirlo al repositorio):

```env
OPENAI_API_KEY=your_key_here
API_BASE_URL=http://localhost:8000
```

Reglas:

- No incluir secretos reales en commits.
- Mantener `.env` fuera de versionado.
- Configurar secretos de produccion solo en Vercel/Jira Vault si aplica.

## Flujo Git -> Build -> URL

1. Crear rama por ticket: `feature/VET-XX`.
2. Implementar cambios y abrir Pull Request contra `main`.
3. Ejecutar validaciones (lint/tests/manuales) antes de merge.
4. Merge a `main`.
5. Verificar build y despliegue en Vercel.
6. Confirmar URL publica funcional.

## Checklist de tickets VET

- [ ] Ticket Jira enlazado en PR.
- [ ] Alcance y CAC revisados antes de implementar.
- [ ] Cambios documentados en `README.MD` o `docs`/`.cursor/docs` cuando aplique.
- [ ] Evidencias de validacion adjuntas (capturas/logs/tests).
- [ ] Estado del ticket actualizado (`Por hacer` -> `En curso` -> `En revision` -> `Listo`).

## Backlog de referencia (TBD)

- Fuente principal: `.cursor/docs/Tickets.md`
- Priorizacion por sprint: TBD
- Dependencias tecnicas: TBD

## Estado del documento

Este README se considera una plantilla viva. Se actualiza progresivamente conforme se implementan tickets VET.