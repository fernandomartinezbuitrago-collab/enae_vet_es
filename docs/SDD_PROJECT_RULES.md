# 📜 Reglas de Trabajo SDD - Clínica Veterinaria

[cite_start]Este documento define las normas de contexto y trazabilidad obligatorias para todos los agentes y desarrolladores del proyecto.

## 1. Contexto del Repositorio
* **Repositorio Principal:** `https://github.com/fernandomartinezbuitrago-collab/enae_vet_es`
* **Rama Principal:** `main`
* [cite_start]**Convención de Ramas:** Todas las tareas deben realizarse en ramas tipo `feature/VET-XX-descripcion-corta`.

## 2. Gestión de Tareas (Jira)
* **Tablero Jira:** `FERNANDO - Enae-vet-es`
* [cite_start]**Clave del Proyecto:** `VET` (o la que aparezca en tus tickets).
* [cite_start]**Regla de Cierre:** No se permite dar por finalizada una implementación sin haber referenciado el ticket de Jira correspondiente en el commit o la PR.

## 3. Normas para Agentes de IA
* [cite_start]**Lectura Obligatoria:** Antes de ejecutar los comandos `/enrich` o `/implement-ticket`, el agente DEBE leer este archivo y el `README.md` para asegurar que el código respeta las reglas del "Tetris" (240 min / 2 perros)[cite: 14, 19].
* [cite_start]**Contexto de Git:** El asistente debe incluir siempre el repositorio y el tablero Jira en su contexto de trabajo activo.

## 4. Definición de Hecho (DoD)
Un ticket se considera "Done" solo si:
1. El código está en `main`.
2. Vercel ha desplegado con éxito.
3. El ticket de Jira ha sido movido manualmente a la columna "Done".
