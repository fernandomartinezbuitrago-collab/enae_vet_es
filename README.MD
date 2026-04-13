# 🐾 Asistente Inteligente - Clínica Veterinaria (MVP)

Este proyecto consiste en el desarrollo de un chatbot inteligente para la gestión de una clínica veterinaria, realizado como proyecto final para el programa de IA Generativa de **ENAE Business School**. El sistema automatiza la atención al cliente, la consulta de instrucciones preoperatorias y la gestión de agenda quirúrgica real.

🚀 **Despliegue público:** [https://enae-vet-es.vercel.app/](https://enae-vet-es.vercel.app/)

---

## 🛠️ Stack Tecnológico

* **Backend:** Python 3.12 con FastAPI.
* **Orquestador de IA:** LangChain v0.3.
* **Modelo de Lenguaje:** Google Gemini 1.5 Flash.
* **Infraestructura:** Vercel (Serverless Functions).
* **Integraciones:** Google Calendar API (v3).
* **Frontend:** HTML5, CSS3 (Tailwind CSS) y JavaScript.

---

## 🧠 Características Principales

### 1. Implementación RAG (Retrieval-Augmented Generation)
El bot utiliza una técnica de RAG dinámico para ofrecer información oficial y actualizada. Mediante `WebBaseLoader`, el asistente extrae las instrucciones preoperatorias directamente de la fuente de verdad de la clínica:
* **URL de conocimiento:** [Instrucciones Preoperatorias](https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation)

### 2. Tool de Disponibilidad Quirúrgica ("El Tetris")
Se ha desarrollado una herramienta personalizada (`tool`) que conecta con **Google Calendar** para gestionar la capacidad del quirófano en tiempo real siguiendo las reglas del SDD:
* **Capacidad Temporal:** Máximo 240 minutos de cirugía al día.
* **Restricción por Especie:** Límite estricto de **2 perros** por día.
* **Días Operativos:** Gestión exclusiva de citas de Lunes a Jueves.

### 3. Memoria de Sesión
El chatbot implementa `InMemoryChatMessageHistory` gestionado por un `session_id`, lo que permite mantener el contexto de la mascota (nombre, especie, edad) durante toda la conversación.

---

## 📋 Reglas de Negocio Implementadas (SDD)

El asistente ha sido programado para cumplir estrictamente con los criterios de la Sesión 6:
* **Analítica Preoperatoria:** Obligatoria para cualquier mascota mayor de 6 años.
* **Protocolo de Ayuno:** 8-12 horas para sólidos; agua permitida hasta 2 horas antes.
* **Gestión de Celo:** Bloqueo de cirugías para perras en celo (requiere espera de 2 meses).
* **Horarios de Logística:**
    * Gatos: Entrada (08:00-09:00) / Recogida (~15:00).
    * Perros: Entrada (09:00-10:30) / Recogida (~12:00).

---

## 📈 Metodología y Trazabilidad

El desarrollo se ha gestionado siguiendo metodologías ágiles y control de versiones:
* **Backlog en Jira:** Seguimiento desde el ticket **VET-1** hasta el **VET-14**.
* **Control de Versiones:** Uso de GitFlow con Pull Requests vinculados a cada tarea de Jira para asegurar la trazabilidad del código.

---

## ⚙️ Configuración del Entorno

Para replicar este proyecto, es necesario configurar las siguientes variables de entorno en Vercel:

```env
GOOGLE_API_KEY=tu_clave_de_google_ai_studio
CALENDAR_API_KEY=tu_clave_de_google_cloud_console

# El ID del calendario se gestiona internamente o vía variable
Intent,Descripción,Ejemplo de Interacción
SALUDO,Inicio de la conversación y presentación del rol., ¡Hola! Soy el asistente de la clínica. ¿En qué puedo ayudarte?
CONSULTAR_SERVICIOS,Información sobre la cartera de servicios de la clínica.,Ofrece cirugía, medicina general, vacunación, peluquería, etc.
PREPARACION_CIRUGIA, Recuperación de información (RAG) sobre ayuno y protocolos.,Ayuno de sólidos (8-12h) y agua (hasta 1-2h antes). 
REGLA_EDAD,Validación de analítica obligatoria por edad., Al tener tu perro 8 años, es obligatoria una analítica preoperatoria.
REGLA_CELO,Gestión de restricciones médicas por celo en perras y gatas.,Diferenciación entre perras (espera de 2 meses) y gatas (sí pueden operarse).
CONSULTAR_CITA, Uso de la Tool de disponibilidad conectada a Google Calendar.,Consulta de huecos disponibles para fechas específicas. 
RESERVA_CAPACIDAD, Control de límites de la agenda (""El Tetris""). Gestión de rechazo ante solicitudes que exceden el cupo diario de perros. 
LOGISTICA_ENTREGA,Gestión de horarios específicos por especie (Memoria).,Horarios de entrega de gatos (08:00-09:00) y confirmación de especie.
EMERGENCIA_DERIVACION,Manejo de casos fuera del alcance del MVP.,Gestión de emergencias médicas y derivación a contacto telefónico.
