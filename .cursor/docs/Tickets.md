Backlog Jira: Caso Clínica Veterinaria

## Épica 1: SET UP

### VET-1: Repositorio base y acceso del equipo
- **Tipo**: Tarea
- **Story Points**: 1
- **Resumen**: Fork del repositorio baseline y acceso del equipo.
- **Descripción**:
  - Realizar fork de `kuuli/veterinary-clinic-chatbot`.
  - Definir rama principal, permisos y añadir al profesor (`jmarco111`) como colaborador.
  - Sin credenciales ni API keys en el historial.
- **Criterios de Aceptación**:
  - URL del repo accesible para el profesor.
  - `README.md` indica autores y enlace al proyecto.
  - `.gitignore` incluye `.env`.
  - No hay secretos en los commits.
- **Entregable**:
  - Enlace al repositorio + confirmación de accesos.

### VET-2: README maestro: estructura y huecos
- **Tipo**: Historia
- **Story Points**: 2
- **Resumen**: Dejar el `README.md` preparado como documento central (plantilla viva).
- **Descripción**:
  - Ampliar el `README` con:
    - Visión del producto (MVP).
    - Miembros del equipo.
    - Enlaces a Jira y Vercel.
    - Guía de instalación.
    - Variables de entorno.
    - Checklist de tickets VET.
- **Criterios de Aceptación**:
  - Estructura por secciones completa.
  - Huecos explícitos para contenido pendiente (TBD).
  - Enlace al proyecto Jira del equipo.
- **Notas**:
  - Se actualiza progresivamente en tickets posteriores.

### VET-3: Configuración y despliegue en Vercel
- **Tipo**: Historia
- **Story Points**: 2
- **Resumen**: Configurar Vercel y verificar despliegue correcto.
- **Descripción**:
  - Conectar repo a Vercel.
  - Configurar variables de entorno solo en el panel.
  - Documentar flujo Git → build → URL.
- **Criterios de Aceptación**:
  - Proyecto vinculado y despliegue exitoso.
  - Variables de entorno definidas solo en Vercel.
  - URL pública accesible y funcional.
- **Entregable**:
  - URL de Vercel + captura de deploy OK.

### VET-14: Documentación de dominio en el repo
- **Tipo**: Historia
- **Story Points**: 2
- **Resumen**: Añadir tres documentos en `docs/` (preparatorio, Event Storming, reglas).
- **Descripción**:
  - Versionar tres artefactos:
    1. Glosario y alcance.
    2. Event Storming con diagrama Mermaid.
    3. Reglas de negocio (tiempos, límites de agenda, etc.).
- **Criterios de Aceptación**:
  - Tres ficheros en `docs/` con contenido sustantivo.
  - Diagrama Mermaid reproducible en GitHub.
  - `README` enlaza a los tres documentos.
- **Entregable**:
  - Enlaces en `README` + rutas de los tres `.md`.

---

## Épica 2: SDD y Flujo de Trabajo

### VET-4: Reglas SDD (Repo + Jira)
- **Tipo**: Tarea
- **Story Points**: 1
- **Resumen**: Documento de reglas SDD: contexto de repositorio y tablero Jira propio.
- **Descripción**:
  - Crear `docs/SDD_PROJECT_RULES.md` definiendo:
    - Convenciones de ramas (`feature/VET-XX`).
    - Inclusión del board Jira en el contexto.
    - Norma de no cerrar tickets sin referencia al repo.
- **Criterios de Aceptación**:
  - Documento accesible y enlazado desde el `README`.
  - URLs explícitas del board y repo.

### VET-5: Comando / skill «enrich»
- **Tipo**: Historia
- **Story Points**: 2
- **Resumen**: Definir y documentar el flujo *enrich* para tickets o specs.
- **Descripción**:
  - Crear procedimiento para ampliar tickets básicos con CAC y riesgos técnicos.
  - Independiente del comando *implementar*.
- **Criterios de Aceptación**:
  - Comando versionado y descrito.
  - Ejemplo antes/después en el repositorio.

### VET-6: Comando / skill «implementar»
- **Tipo**: Historia
- **Story Points**: 2
- **Resumen**: Definir flujo *implementar*: de ticket a código.
- **Descripción**:
  - Crear comando en `.cursor/commands/` que guíe la implementación asumiendo perfiles de Backend, Frontend y Product Manager.
- **Criterios de Aceptación**:
  - Instrucciones claras de invocación.
  - Enumeración de dependencias de skills (BE, FE, PM).

---

## Épica 3: CHATBOT

### VET-7: API FastAPI con dos endpoints
- **Tipo**: Historia
- **Story Points**: 1
- **Resumen**: FastAPI mínima con Swagger y esquemas.
- **Descripción**:
  - Crear esqueleto con dos rutas (salud y chat/prueba) usando Pydantic.
  - Generar `/docs` automático.
- **Criterios de Aceptación**:
  - `requirements.txt` con FastAPI y uvicorn.
  - Swagger accesible.
  - `README` explica cómo arrancar el servidor.

### VET-8: Interfaz simple de chat inyectable
- **Tipo**: Historia
- **Story Points**: 1
- **Resumen**: UI mínima de chat conectable al backend.
- **Descripción**:
  - Implementar pantalla HTML/Jinja básica que envíe mensajes al endpoint del backend.
- **Criterios de Aceptación**:
  - Interfaz usable en navegador.
  - Configuración de URL del API vía variable de entorno.

### VET-9: Chatbot simple ask bot
- **Tipo**: Historia
- **Story Points**: 2
- **Resumen**: Flujo mínimo pregunta → LLM con API Key.
- **Descripción**:
  - Lógica de backend que recibe texto y llama al modelo.
  - El *system prompt* usa un *placeholder* referenciando el `prompt.md` oficial.
- **Criterios de Aceptación**:
  - Respuesta generada desde el LLM en local.
  - API Key solo vía `.env`.

### VET-10: Memoria de conversación por `session_id`
- **Tipo**: Historia
- **Story Points**: 2
- **Resumen**: Persistencia de contexto por sesión.
- **Descripción**:
  - Añadir historial de turnos asociado a un ID único (cabecera o JSON).
- **Criterios de Aceptación**:
  - Sesiones distintas no comparten historial.
  - Mantiene coherencia en varios turnos.

### VET-11: RAG con fuente URL oficial
- **Tipo**: Historia
- **Story Points**: 2
- **Resumen**: RAG basado en la página oficial de instrucciones preoperatorias.
- **Descripción**:
  - Ingerir contenido de la oficial para responder sobre ayuno y preparación.
- **Criterios de Aceptación**:
  - Fuente principal es la URL indicada.
  - *Retriever* demostrable (logs/capturas).

### VET-12: Tool «comprobar disponibilidad» (Mock)
- **Tipo**: Historia
- **Story Points**: 2
- **Resumen**: Herramienta de disponibilidad con respuestas simuladas.
- **Descripción**:
  - Crear función invocable por el agente que devuelva datos fijos (JSON) coherentes con las reglas del dominio (días laborables).
- **Criterios de Aceptación**:
  - El agente puede invocar la *tool* y procesar su salida.

### VET-13: Integración con calendario real
- **Tipo**: Historia
- **Story Points**: 3
- **Resumen**: Sustituir *mock* con Google Calendar / Calendly.
- **Descripción**:
  - Conectar la *tool* a una API real para listar o crear eventos.
  - Mapear limitaciones respecto a las reglas de 240 min.
- **Criterios de Aceptación**:
  - Llamada real a API (no estática).
  - Evidencia de consulta exitosa (log/vídeo).

