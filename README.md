# Sistema de Registro de Notas Académicas
**Universidad Regional del Sur | Pruebas de Software — Semestre V**

**Tecnología elegida:** Python 3.11 + `uv` + `pytest` + `pytest-bdd`

**Justificación:** Lo elegi porque es el stack tecnologico que hemos visto en clase, entonces no me quiero complicar y uso el mismo

---

## Parte 1 — Análisis de Pruebas

### 1.1 Particiones de Equivalencia — Requerimiento 1 (Nota entre 0.0 y 5.0)

| Partición | Rango | Valor Representativo | Resultado Esperado |
|---|---|---|---|
| Válida — rango bajo | 0.0 < nota < 3.0 | 1.5 | Nota registrada exitosamente |
| Válida — rango alto | 3.0 ≤ nota < 5.0 | 4.0 | Nota registrada exitosamente |
| Inválida — bajo el mínimo | nota < 0.0 | -1.0 | `InvalidGradeError` |
| Inválida — sobre el máximo | nota > 5.0 | 6.0 | `InvalidGradeError` |
| Válida — exactamente el mínimo | nota = 0.0 | 0.0 | Nota registrada exitosamente |
| Válida — exactamente el máximo | nota = 5.0 | 5.0 | Nota registrada exitosamente |

### 1.2 Análisis de Valores Límite — Requerimiento 1

| Valor | Posición | ¿Dentro del rango? | Resultado Esperado |
|---|---|---|---|
| -0.1 | Justo antes del mínimo | No | `InvalidGradeError` |
| 0.0 | Límite inferior exacto | Sí | Nota registrada exitosamente |
| 0.1 | Justo después del mínimo | Sí | Nota registrada exitosamente |
| 4.9 | Justo antes del máximo | Sí | Nota registrada exitosamente |
| 5.0 | Límite superior exacto | Sí | Nota registrada exitosamente |
| 5.1 | Justo después del máximo | No | `InvalidGradeError` |

### 1.3 Preguntas al Product Owner — Requerimiento 4

**Pregunta 1:** ¿Qué formato identifica un semestre? ¿Es un string libre como "2024-1" o hay un catálogo definido con validaciones propias?

*Justificación:* Si el semestre es string libre, "2024-1" y "2024-I" serían semestres distintos aunque el usuario quisiera decir lo mismo, esto impacta directamente el diseño de casos de prueba porque necesitamos saber si debemos probar variaciones de formato o asumir que el sistema siempre recibe un valor ya validado

**Pregunta 2:** Si un estudiante pierde una materia en "2024-1" y la vuelve a cursar en "2024-2", ¿el historial anterior se mantiene para el cálculo del promedio o solo cuenta la nota más reciente?

*Justificación:* Esta decisión cambia radicalmente los casos de prueba del requerimiento 3 porque si el promedio solo cuenta la nota más reciente por materia necesito casos que verifiquen que notas anteriores se ignoran, si se cuentan todas, el resultado del promedio con materia repetida en semestres distintos es diferente

---

## Parte 2 — Casos de Prueba Formales

| ID | Requerimiento | Descripción | Precondición | Datos de entrada | Pasos | Resultado esperado | Tipo |
|---|---|---|---|---|---|---|---|
| TC01 | REQ-1 | Registro de nota válida en rango normal | Sistema limpio | materia="Matemáticas", semestre="2024-1", nota=3.5 | 1. Llamar `register_grade("Matemáticas","2024-1",3.5)` | Nota almacenada sin error | Positivo |
| TC02 | REQ-1 | Nota negativa rechazada | Sistema limpio | materia="Física", semestre="2024-1", nota=-1.0 | 1. Llamar `register_grade("Física","2024-1",-1.0)` | Se lanza `InvalidGradeError` | Negativo |
| TC03 | REQ-1 | Nota mayor a 5.0 rechazada | Sistema limpio | materia="Historia", semestre="2024-1", nota=6.0 | 1. Llamar `register_grade("Historia","2024-1",6.0)` | Se lanza `InvalidGradeError` | Negativo |
| TC04 | REQ-1 | Nota exactamente 0.0 aceptada | Sistema limpio | materia="Arte", semestre="2024-1", nota=0.0 | 1. Llamar `register_grade("Arte","2024-1",0.0)` | Nota almacenada sin error | Borde |
| TC05 | REQ-1 | Nota exactamente 5.0 aceptada | Sistema limpio | materia="Química", semestre="2024-1", nota=5.0 | 1. Llamar `register_grade("Química","2024-1",5.0)` | Nota almacenada sin error | Borde |
| TC06 | REQ-2 | Estudiante aprueba con nota 3.5 | Nota 3.5 en Matemáticas 2024-1 | materia="Matemáticas", semestre="2024-1" | 1. Llamar `is_passing("Matemáticas","2024-1")` | Retorna `True` | Positivo |
| TC07 | REQ-2 | Estudiante reprueba con nota 2.9 | Nota 2.9 en Historia 2024-1 | materia="Historia", semestre="2024-1" | 1. Llamar `is_passing("Historia","2024-1")` | Retorna `False` | Negativo |
| TC08 | REQ-2 | Nota exactamente 3.0 aprueba | Nota 3.0 en Física 2024-1 | materia="Física", semestre="2024-1" | 1. Llamar `is_passing("Física","2024-1")` | Retorna `True` | Borde |
| TC09 | REQ-3 | Promedio sin notas es 0.0 | Sistema limpio, sin notas | Ninguno | 1. Llamar `get_average()` | Retorna `0.0` | Positivo |
| TC10 | REQ-3 | Promedio de una sola nota | Nota 4.0 en Matemáticas 2024-1 | Ninguno | 1. Llamar `get_average()` | Retorna `4.0` | Positivo |
| TC11 | REQ-3 | Promedio correcto con múltiples notas | Notas 4.0 y 2.0 registradas | Ninguno | 1. Llamar `get_average()` | Retorna `3.0` | Positivo |
| TC12 | REQ-4 | Error al duplicar nota misma materia mismo semestre | Nota 4.0 en Matemáticas 2024-1 | materia="Matemáticas", semestre="2024-1", nota=3.0 | 1. Intentar `register_grade("Matemáticas","2024-1",3.0)` | Se lanza `DuplicateGradeError` | Negativo |
| TC13 | REQ-4 | Permite misma materia en semestre diferente | Nota 4.0 en Matemáticas 2024-1 | materia="Matemáticas", semestre="2024-2", nota=3.5 | 1. Llamar `register_grade("Matemáticas","2024-2",3.5)` | Nota registrada exitosamente | Positivo |
| TC14 | REQ-4 | Permite materia diferente en mismo semestre | Nota 4.0 en Matemáticas 2024-1 | materia="Historia", semestre="2024-1", nota=3.5 | 1. Llamar `register_grade("Historia","2024-1",3.5)` | Nota registrada exitosamente | Positivo |