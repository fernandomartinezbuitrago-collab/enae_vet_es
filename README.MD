# 🐾 Chatbot Clínica Veterinaria - MVP Esterilización

[cite_start]Este proyecto es un asistente inteligente diseñado para optimizar el agendamiento de cirugías de castración y esterilización, reduciendo la carga administrativa de la clínica[cite: 473].

---

## 🔗 1. Ecosistema de Trabajo

 *[cite_start]**Tablero Jira (Épicas VET):** [PEGA AQUÍ EL ENLACE A TU PROYECTO JIRA] [cite: 604]

 *[cite_start]**Despliegue (Vercel):** [PEGA AQUÍ TU URL DE VERCEL] [cite: 514, 607]

 *[cite_start]**Documentación API:** `[URL-VERCEL]/docs` (Swagger/OpenAPI) [cite: 627, 628]

---

## 🧠 2. Reglas de Negocio ("El Tetris")

[cite_start]El chatbot está programado para cumplir estrictamente con la capacidad operativa de la clínica[cite: 78, 79]:

 *[cite_start]**Capacidad Diaria:** Máximo de **240 minutos** quirúrgicos de lunes a jueves[cite: 82, 99].

 *[cite_start]**Límite de Especie:** Máximo **2 perros** por día, sin importar los minutos restantes[cite: 102, 105].

* **Ventanas de Entrega:**

     *[cite_start]**Gatos:** 08:00 - 09:00 (Lunes a Viernes)[cite: 111, 120].

     *[cite_start]**Perros:** 09:00 - 10:30 (Lunes a Jueves)[cite: 111, 121].

---

## 📚 3. Implementación RAG (+1 pt)

[cite_start]El conocimiento del bot sobre ayuno y protocolos preoperatorios se alimenta de la fuente oficial[cite: 516, 517]:

 *[cite_start]**Fuente:** [Instrucciones Preoperatorias Oficiales]([https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation)[cite](https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation)[cite): 517, 639].

---

## 🛠️ 4. Instalación y Uso

1. [cite_start]**Requisitos:** Python 3.10+ y `pip install -r requirements.txt`[cite: 544, 627].

2. [cite_start]**Variables de Entorno:** Configurar `.env` con `OPENAI_API_KEY` (Ver `.env.example`)[cite: 199, 633].

3. [cite_start]**Ejecutar:** `uvicorn main:app --reload`[cite: 627].

---

## 📊 5. Backlog de Tareas (Trazabilidad)

| Ticket | Tarea | Estado |

| :--- | :--- | :--- |

| **VET-1** | Fork y accesos al profesor `jmarco111`) | [cite_start]Hecho ✅ [cite: 601] |

| **VET-2** | README Maestro (Estructura) | [cite_start]En curso 🛠️ [cite: 604] |

| **VET-14** | Docs de dominio (Event Storming/Reglas) | [cite_start]Pendiente ⏳  |

| **VET-3** | Despliegue en Vercel | [cite_start][Pendiente/Hecho] [cite: 607] |