# 🐾 Chatbot Clínica Veterinaria - MVP Esterilización

Este proyecto es un asistente inteligente diseñado para optimizar el agendamiento de cirugías de castración y esterilización, reduciendo la carga administrativa de la clínica[cite: 473].

---

## 🔗 1. Ecosistema de Trabajo

 **Tablero Jira (Épicas VET):**  [https://fernandomartinezbuitrago.atlassian.net/jira/software/projects/FERNANDO/summary?atlOrigin=eyJpIjoiZmUxMTAwNmFhNzg5NGIwMTg5OWY3YmIxODEwMTU5MGEiLCJwIjoiaiJ9](https://fernandomartinezbuitrago.atlassian.net/jira/software/projects/FERNANDO/summary?atlOrigin=eyJpIjoiZmUxMTAwNmFhNzg5NGIwMTg5OWY3YmIxODEwMTU5MGEiLCJwIjoiaiJ9)

 **Despliegue (Vercel):** [PEGA AQUÍ TU URL DE VERCEL]

 **Documentación API:** `[URL-VERCEL]/docs` (Swagger/OpenAPI)

## 🧠 2. Reglas de Negocio ("El Tetris")

]El chatbot está programado para cumplir estrictamente con la capacidad operativa de la clínica

*Capacidad Diaria:** Máximo de **240 minutos** quirúrgicos de lunes a jueves[

*Límite de Especie:** Máximo **2 perros** por día, sin importar los minutos restantes

 *Perros:** 09:00 - 10:30 (Lunes a Jueves).

---

## 📚 3. Implementación RAG (+1 pt)

El conocimiento del bot sobre ayuno y protocolos preoperatorios se alimenta de la fuente oficial[cite: 516, 517]:

 [Instrucciones Preoperatorias Oficiales]([https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation)](https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation)[cite).

---

## 🛠️ 4. Instalación y Uso

1. **Requisitos:** Python 3.10+ y `pip install -r requirements.txt`[cite: 544, 627].

2.**Variables de Entorno:** Configurar `.env` con `OPENAI_API_KEY` (Ver `.env.example`).

3. **Ejecutar:** `uvicorn main:app --reload`.

---

## 📊 5. Backlog de Tareas (Trazabilidad)

| Ticket | Tarea | Estado |

| :--- | :--- | :--- |

| **VET-1** | Fork y accesos al profesor `jmarco111`) | [cite_start]Hecho ✅ 

| **VET-2** | README Maestro (Estructura) | [cite_start]En curso 🛠️

| **VET-14** | Docs de dominio (Event Storming/Reglas) | [cite_start]Pendiente ⏳  |

| **VET-3** | Despliegue en Vercel | [cite_start][Pendiente/Hecho]