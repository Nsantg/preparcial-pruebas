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