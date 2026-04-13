# 🐾 Asistente Inteligente - Clínica Veterinaria

Este proyecto consiste en el desarrollo de un chatbot inteligente para la gestión de una clínica veterinaria, realizado como proyecto final para el programa de IA Generativa de **ENAE Business School**. El sistema automatiza la atención al cliente, la consulta de instrucciones preoperatorias y la gestión de agenda quirúrgica real mediante agentes.

🚀 **Despliegue público:** [https://enae-vet-es.vercel.app/](https://enae-vet-es.vercel.app/)

---

## 🛠️ Stack Tecnológico y Dependencias

El proyecto utiliza un entorno de ejecución basado en **Python 3.12** y las versiones más recientes del ecosistema de IA generativa:

* **Framework Web:** FastAPI (v0.111.0) y Uvicorn.
* **Orquestador de IA:** LangChain (v0.3.7) y LangChain-Core (v0.3.19).
* **Modelo de Lenguaje:** Google **Gemini 2.5 Flash** (vía `langchain-google-genai` v2.0.7).
* **Gestión de Datos:** Pydantic (v2.7.4) para validación de esquemas.
* **Extracción de Conocimiento (RAG):** WebBaseLoader y BeautifulSoup4.
* **Infraestructura:** Vercel (Serverless Functions).

---

## 🧠 Características Principales

### 1. Implementación RAG (Retrieval-Augmented Generation)
El bot utiliza una técnica de RAG dinámico para ofrecer información oficial. Mediante `WebBaseLoader`, el asistente extrae las instrucciones preoperatorias directamente de la URL de conocimiento oficial:
* **Fuente:** [Instrucciones Preoperatorias](https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation)

### 2. Agente con Tool de Calendario Real ("El Tetris")
Se ha implementado un `tool_calling_agent` que utiliza la función `comprobar_disponibilidad`. Esta herramienta conecta con la **API de Google Calendar** para validar la agenda bajo las reglas de negocio:
* **Capacidad:** Máximo de 2 mascotas por día.
* **Días Operativos:** Lunes a Jueves de 08:00 a 14:00.

### 3. Memoria Persistente de Sesión
Mediante `RunnableWithMessageHistory` e `InMemoryChatMessageHistory`, el sistema mantiene el contexto de la conversación (nombre de mascota, especie, etc.) utilizando un `session_id` único por usuario.

---

## 📋 Reglas de Negocio Implementadas (SDD)

El asistente aplica estrictamente las reglas definidas en el **Caso VET**:
* **Analítica Preoperatoria:** Obligatoria para mascotas mayores de 6 años.
* **Protocolo de Ayuno:** Sólidos (8-12h antes) y líquidos (hasta 1-2h antes).
* **Gestión de Celo:** Las gatas pueden operarse; las perras deben esperar 2 meses tras el celo.
* **Logística de Entregas:**
    * **Gatos:** 08:00 - 09:00 (Lun-Vie).
    * **Perros:** 09:00 - 10:30 (Lun-Jue).

---

## 📂 Catálogo de Intents y Casos de Uso

| Intent | Descripción | Ejemplo de Interacción |
| :--- | :--- | :--- |
| **SALUDO** | Inicio de conversación y asignación de rol. | "¡Hola! Soy el asistente de la clínica..." |
| **CONSULTAR_SERVICIOS** | Información sobre servicios generales. | "Ofrecemos cirugía, medicina general, vacunación..." |
| **PREPARACION_CIRUGIA** | Recuperación de datos vía RAG. | "El animal debe ayunar de sólidos entre 8 y 12h." |
| **REGLA_EDAD** | Validación médica por edad (>6 años). | "Al tener 8 años, la analítica es obligatoria." |
| **REGLA_CELO** | Restricciones por ciclo reproductivo. | "Las perras no pueden operarse en celo." |
| **CONSULTAR_CITA** | Uso de Tool (Google Calendar). | "Sí, tenemos 2 huecos disponibles para mañana." |
| **RESERVA_CAPACIDAD** | Lógica de cupo máximo ("El Tetris"). | "Lo siento, el día está completo (máximo 2 citas)." |
| **LOGISTICA_ENTREGA** | Horarios por especie y memoria. | "Los gatos se entregan de 08:00 a 09:00." |
| **EMERGENCIA** | Derivación a contacto humano. | "Puedes llamar a la clínica al 555-123-4567." |

---

## ⚙️ Configuración del Entorno

Para el despliegue, se han configurado las siguientes variables de entorno:

```env
GOOGLE_API_KEY=tu_clave_de_google_ai_studio
CALENDAR_API_KEY=tu_clave_de_google_cloud_console
