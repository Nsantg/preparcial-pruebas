Feature: Registro de notas académicas
  Como estudiante de la Universidad Regional del Sur
  Quiero registrar mis notas por materia y semestre
  Para conocer mi rendimiento académico, saber si apruebo o repruebo
  y calcular mi promedio general al final del período.

  Background:
    Given un estudiante sin notas registradas

  @smoke
  Scenario: El estudiante aprueba una materia con nota suficiente
    When el estudiante registra una nota de 3.5 en "Matemáticas" para el semestre "2024-1"
    Then el estudiante aprueba "Matemáticas" en el semestre "2024-1"

  @smoke
  Scenario: El estudiante reprueba una materia con nota insuficiente
    When el estudiante registra una nota de 2.9 en "Historia" para el semestre "2024-1"
    Then el estudiante reprueba "Historia" en el semestre "2024-1"

  @critical
  Scenario: La nota exactamente en 3.0 es suficiente para aprobar
    When el estudiante registra una nota de 3.0 en "Física" para el semestre "2024-1"
    Then el estudiante aprueba "Física" en el semestre "2024-1"

  @critical
  Scenario Outline: Verificación de aprobación para diferentes notas y materias
    When el estudiante registra una nota de <nota> en "<materia>" para el semestre "2024-1"
    Then el resultado en "<materia>" semestre "2024-1" es <resultado>

    Examples:
      | nota | materia    | resultado |
      | 5.0  | Química    | aprueba   |
      | 3.0  | Biología   | aprueba   |
      | 2.9  | Arte       | reprueba  |
      | 0.0  | Música     | reprueba  |

  @regression
  Scenario: El promedio de un estudiante sin notas es cero
    Then el promedio del estudiante es 0.0

  @regression
  Scenario: El promedio se calcula correctamente con varias materias
    When el estudiante registra una nota de 4.0 en "Matemáticas" para el semestre "2024-1"
    And el estudiante registra una nota de 2.0 en "Historia" para el semestre "2024-1"
    Then el promedio del estudiante es 3.0

  @critical
  Scenario: No se puede registrar dos notas para la misma materia en el mismo semestre
    Given el estudiante ya tiene registrada una nota de 4.0 en "Matemáticas" en el semestre "2024-1"
    When el estudiante intenta registrar una nota de 3.0 en "Matemáticas" para el semestre "2024-1"
    Then el sistema lanza un error de nota duplicada

  @regression
  Scenario: Se puede registrar la misma materia en semestres diferentes
    Given el estudiante ya tiene registrada una nota de 2.0 en "Matemáticas" en el semestre "2024-1"
    When el estudiante registra una nota de 3.5 en "Matemáticas" para el semestre "2024-2"
    Then el estudiante aprueba "Matemáticas" en el semestre "2024-2"