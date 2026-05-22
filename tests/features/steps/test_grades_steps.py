import pytest
from pytest_bdd import given, when, then, parsers, scenarios

from src.grade_system import GradeSystem, DuplicateGradeError, InvalidGradeError

scenarios("grades.feature")


# ─── Fixture compartido de contexto ───────────────────────────────────────────

@given("un estudiante sin notas registradas", target_fixture="student_context")
def student_no_grades():
    """Crea un contexto limpio con un estudiante nuevo."""
    return {
        "student": GradeSystem(),
        "error": None,
        "last_subject": None,
        "last_semester": None,
    }


# ─── Given steps adicionales ──────────────────────────────────────────────────

@given(
    parsers.parse(
        'el estudiante ya tiene registrada una nota de {grade:f} '
        'en "{subject}" en el semestre "{semester}"'
    )
)
def student_has_existing_grade(student_context, grade, subject, semester):
    """Registra una nota preexistente para un escenario."""
    student_context["student"].register_grade(subject, semester, grade)


# ─── When steps ───────────────────────────────────────────────────────────────

@when(
    parsers.parse(
        'el estudiante registra una nota de {grade:f} '
        'en "{subject}" para el semestre "{semester}"'
    )
)
def register_grade(student_context, grade, subject, semester):
    """Registra una nota exitosamente y guarda el contexto para steps posteriores."""
    student_context["student"].register_grade(subject, semester, grade)
    student_context["last_subject"] = subject
    student_context["last_semester"] = semester


@when(
    parsers.parse(
        'el estudiante intenta registrar una nota de {grade:f} '
        'en "{subject}" para el semestre "{semester}"'
    )
)
def attempt_register_duplicate_grade(student_context, grade, subject, semester):
    """Intenta registrar una nota que puede fallar; captura el error si ocurre."""
    try:
        student_context["student"].register_grade(subject, semester, grade)
    except DuplicateGradeError as e:
        student_context["error"] = e


# ─── Then steps ───────────────────────────────────────────────────────────────

@then(parsers.parse('el estudiante aprueba "{subject}" en el semestre "{semester}"'))
def student_passes_subject(student_context, subject, semester):
    assert student_context["student"].is_passing(subject, semester) is True


@then(parsers.parse('el estudiante reprueba "{subject}" en el semestre "{semester}"'))
def student_fails_subject(student_context, subject, semester):
    assert student_context["student"].is_passing(subject, semester) is False


@then(parsers.parse('el resultado en "{subject}" semestre "{semester}" es {resultado}'))
def check_passing_result_outline(student_context, subject, semester, resultado):
    """Verifica el resultado de aprobación para el Scenario Outline."""
    result = student_context["student"].is_passing(subject, semester)
    if resultado == "aprueba":
        assert result is True, f"Se esperaba aprobación pero reprobó en {subject}"
    else:
        assert result is False, f"Se esperaba reprobación pero aprobó en {subject}"


@then(parsers.parse("el promedio del estudiante es {expected:f}"))
def check_average(student_context, expected):
    assert student_context["student"].get_average() == pytest.approx(expected)


@then("el sistema lanza un error de nota duplicada")
def system_raises_duplicate_error(student_context):
    assert isinstance(student_context["error"], DuplicateGradeError), (
        "Se esperaba DuplicateGradeError pero no se lanzó ningún error"
    )