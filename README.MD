# 🐾 Chatbot Clinica Veterinaria - Documento Maestro (Fuente de la Verdad)

Este `README.MD` es la referencia principal del proyecto para alcance funcional, reglas de negocio, stack tecnico, flujo operativo y estado del backlog.

## 🎯 Vision del Proyecto (MVP Esterilizaciones)

El proyecto implementa un chatbot para una clinica veterinaria enfocada en medicina preventiva, especialmente esterilizaciones caninas y felinas.  
El MVP prioriza tres objetivos:

- Guiar al cliente con informacion preoperatoria clara y segura.
- Reducir carga administrativa en la reserva y confirmacion de citas.
- Validar disponibilidad segun reglas estrictas de agenda ("El Tetris") antes de confirmar.

Alcance del MVP:

- Reservas de esterilizacion (perros y gatos).
- Validacion automatica de cupos por minutos y limite de perros por dia.
- Mensajeria de confirmacion con ventana de entrega y protocolo de ayuno.

## 📚 Documentacion de Dominio

Fuente funcional y de negocio del proyecto:

- [`docs/SDD_PROJECT_RULES.md`](docs/SDD_PROJECT_RULES.md): reglas SDD, trazabilidad Jira/GitHub y convenciones de ramas (VET-4).
- `[docs/preparatorio.md](docs/preparatorio.md)`: contexto clinico, protocolo pre y post operatorio, requisitos para una esterilizacion segura.
- `[docs/reglas_negocio.md](docs/reglas_negocio.md)`: reglas formales de agenda, tabla maestra de tiempos y restricciones del algoritmo.
- `[docs/event_storming.md](docs/event_storming.md)`: diagrama del flujo end-to-end (comandos, eventos, politicas y validaciones).

## 🧠 Reglas de Negocio (El Tetris)

Resumen ejecutivo basado en `docs/reglas_negocio.md`:

- **Capacidad diaria maxima:** `240 minutos` por dia quirurgico.
- **Dias operativos para cirugia:** lunes a jueves.
- **Limite de perros:** maximo `2 perros` por dia (aunque sobren minutos).
- **Gatos:** sin limite de cantidad; se limita solo por minutos disponibles.

### Tiempos de cirugia (coste en minutos)

- **Gato macho:** 12 min
- **Gata hembra:** 15 min
- **Perro macho (cualquier peso):** 30 min
- **Perra 0-10 kg:** 45 min
- **Perra 10-20 kg:** 50 min
- **Perra 20-30 kg:** 60 min
- **Perra 30-40 kg:** 60 min
- **Perra >40 kg:** 70 min

### Reglas de bloqueo

Una fecha solo es valida si se cumplen ambas condiciones:

1. `(minutos_ocupados + minutos_nueva_cita) <= 240`
2. Si la especie es perro: `(perros_del_dia + 1) <= 2`

Si falla cualquiera de las dos, la fecha se marca como **No disponible**.

## 🛠️ Stack Tecnico

- **Backend API:** FastAPI
- **Orquestacion IA:** LangChain
- **Modelo LLM:** OpenAI
- **Despliegue:** Vercel ([https://enae-vet-es.vercel.app](https://enae-vet-es.vercel.app))

## ⚙️ Comandos Operativos (.cursor/commands)

### `/enrich`

Comando para enriquecer tickets Jira existentes (especialmente para PM):

- Completa descripcion con arquitectura, tecnologias, flujo, glosario de docs, out of scope y CAC.
- Mejora claridad y trazabilidad antes de implementar.

Referencia: `.cursor/commands/enrich.md`

### `/implement-ticket`

Comando para ejecutar tickets de punta a punta:

- Lee ticket y CAC.
- Implementa cambios en codigo/documentacion.
- Ejecuta validaciones.
- Prepara rama/PR y acompana el flujo de estados Jira.

Referencia: `.cursor/commands/implement-ticket.md`

## 📊 Estado del Backlog (VET)


| Ticket         | Descripcion                          | Estado      |
| -------------- | ------------------------------------ | ----------- |
| VET-1          | Repo base y accesos                  | Hecho ✅     |
| VET-2          | README Maestro                       | Hecho ✅     |
| VET-14         | Documentacion de dominio             | Hecho ✅     |
| VET-4          | Reglas SDD (Repo + Jira)             | Hecho ✅     |
| VET-3          | Configuracion y despliegue en Vercel | Pendiente ⏳ |
| VET-7 a VET-13 | Implementacion del chatbot           | Pendiente ⏳ |


Backlog detallado: `.cursor/docs/Tickets.md`

## 🔗 Enlaces de Proyecto

- Jira (proyecto): [FERNANDO - Enae-vet-es](https://fernandomartinezbuitrago.atlassian.net/jira/software/projects/FERNANDO/summary)
- Ticket VET-2 equivalente en Jira: [FERNANDO-14](https://fernandomartinezbuitrago.atlassian.net/browse/FERNANDO-14)
- Ticket VET-3 equivalente en Jira: [FERNANDO-15](https://fernandomartinezbuitrago.atlassian.net/browse/FERNANDO-15)

## ✅ Criterio de Mantenimiento del README

Cada cambio funcional relevante debe reflejarse aqui para mantener este documento como **fuente de la verdad** del proyecto.