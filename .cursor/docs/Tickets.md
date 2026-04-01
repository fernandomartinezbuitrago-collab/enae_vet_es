📋 Backlog Jira: Caso Clínica Veterinaria
Épica 1: SET UP
VET-1: Repositorio base y acceso del equipo ✅
Estado: Hecho

Resumen: Fork del repo y acceso al profesor.

Criterios: URL accesible, .gitignore configurado, sin secretos en historial.

VET-2: README maestro: estructura y visión ✅
Estado: Hecho

Resumen: README con visión, equipo, enlaces y tabla de tickets.

Criterios: Documento centralizado y actualizado.

VET-3: Configuración y despliegue en Vercel ✅
Estado: Hecho

Resumen: Conectar repo a Vercel y configurar variables de entorno.

Criterios: URL pública funcionando (https://enae-vet-es.vercel.app).

VET-14: Documentación de dominio en el repo ✅
Estado: Hecho

Resumen: Tres documentos en docs/ (preparatorio, Event Storming, reglas).

Criterios: Diagrama Mermaid funcional y enlaces en el README.

Épica 2: SDD y Flujo de Trabajo
VET-4: Reglas SDD (Repo + Jira) ✅
Estado: Hecho

Resumen: Documento de reglas de trazabilidad y contexto de agentes.

Criterios: Archivo SDD_PROJECT_RULES.md creado y enlazado.

VET-5: Comando / skill «enrich» ✅
Estado: Hecho

Resumen: Definir el flujo para ampliar tickets con IA.

Criterios: Archivo .cursor/commands/enrich.md funcional.

VET-6: Comando / skill «implementar» ⏳
Estado: Pendiente

Resumen: Definir flujo de implementación técnica automática.

Criterios: Archivo .cursor/commands/implement-ticket.md configurado.

Épica 3: CHATBOT (MVP)
VET-7: API FastAPI con dos endpoints ⏳
Estado: Pendiente

Resumen: Crear servidor con rutas de salud y chat.

VET-8: Interfaz simple de chat inyectable ⏳
Estado: Pendiente

Resumen: UI mínima (HTML/JS) para hablar con el bot.

VET-9: Chatbot simple «ask bot» ⏳
Estado: Pendiente

Resumen: Integración con OpenAI para respuestas básicas.

VET-10: Memoria de conversación (Session ID) ⏳
Estado: Pendiente

Resumen: Mantener el contexto de la charla entre mensajes.

VET-11: RAG con fuente URL oficial ⏳
Estado: Pendiente

Resumen: Consultar la web de la clínica para dar instrucciones de ayuno reales.

VET-12: Tool «comprobar disponibilidad» (Mock) ⏳
Estado: Pendiente

Resumen: Función que simula mirar la agenda del veterinario.

VET-13: Integración con calendario real ⏳
Estado: Pendiente

Resumen: Conexión con API de Google Calendar o similar.

VET-15: Monitorización y Cierre de MVP ⏳
Estado: Pendiente

Resumen: Pruebas de QA finales y actualización de URL en README.

