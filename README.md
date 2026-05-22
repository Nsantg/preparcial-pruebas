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

---

## Parte 3 — Cobertura de Tests

```
 Built grade-system @ file:///C:/Users/Santi/Desktop/grade-system
Installed 11 packages in 290ms
=============================================================================== test session starts ===============================================================================
platform win32 -- Python 3.13.13, pytest-9.0.3, pluggy-1.6.0 -- C:\Users\Santi\Desktop\grade-system\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Santi\Desktop\grade-system
configfile: pyproject.toml
testpaths: tests
plugins: bdd-8.1.0, cov-7.1.0
collected 20 items                                                                                                                                                                 

tests/test_grade_system.py::TestRegisterGrade::test_register_valid_grade_stores_successfully PASSED                                                                          [  5%]
tests/test_grade_system.py::TestRegisterGrade::test_register_negative_grade_raises_invalid_error PASSED                                                                      [ 10%]
tests/test_grade_system.py::TestRegisterGrade::test_register_grade_above_maximum_raises_invalid_error PASSED                                                                 [ 15%]
tests/test_grade_system.py::TestRegisterGrade::test_register_grade_at_minimum_boundary_zero_is_valid PASSED                                                                  [ 20%]
tests/test_grade_system.py::TestRegisterGrade::test_register_grade_at_maximum_boundary_five_is_valid PASSED                                                                  [ 25%]
tests/test_grade_system.py::TestRegisterGrade::test_register_grade_just_below_minimum_raises_invalid_error PASSED                                                            [ 30%]
tests/test_grade_system.py::TestRegisterGrade::test_register_grade_just_above_maximum_raises_invalid_error PASSED                                                            [ 35%]
tests/test_grade_system.py::TestPassingStatus::test_grade_above_three_returns_passing PASSED                                                                                 [ 40%]
tests/test_grade_system.py::TestPassingStatus::test_grade_below_three_returns_failing PASSED                                                                                 [ 45%]
tests/test_grade_system.py::TestPassingStatus::test_grade_exactly_three_returns_passing PASSED                                                                               [ 50%]
tests/test_grade_system.py::TestPassingStatus::test_grade_zero_returns_failing PASSED                                                                                        [ 55%]
tests/test_grade_system.py::TestPassingStatus::test_grade_five_returns_passing PASSED                                                                                        [ 60%]
tests/test_grade_system.py::TestAverage::test_average_with_no_grades_returns_zero PASSED                                                                                     [ 65%]
tests/test_grade_system.py::TestAverage::test_average_with_single_grade_returns_that_grade PASSED                                                                            [ 70%]
tests/test_grade_system.py::TestAverage::test_average_with_multiple_grades_returns_correct_average PASSED                                                                    [ 75%]
tests/test_grade_system.py::TestAverage::test_average_with_three_grades_returns_correct_average PASSED                                                                       [ 80%]
tests/test_grade_system.py::TestDuplicateGrade::test_register_duplicate_grade_same_subject_same_semester_raises_error PASSED                                                 [ 85%]
tests/test_grade_system.py::TestDuplicateGrade::test_register_same_subject_different_semester_is_allowed PASSED                                                              [ 90%]
tests/test_grade_system.py::TestDuplicateGrade::test_register_different_subjects_same_semester_is_allowed PASSED                                                             [ 95%]
tests/test_grade_system.py::TestDuplicateGrade::test_duplicate_grade_error_message_is_descriptive PASSED                                                                     [100%]

================================================================================= tests coverage ==================================================================================
________________________________________________________________ coverage: platform win32, python 3.13.13-final-0 _________________________________________________________________

Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src\__init__.py           0      0   100%
src\grade_system.py      28      1    96%   37
---------------------------------------------------
TOTAL                    28      1    96%
=============================================================================== 20 passed in 0.12s ================================================================================
```