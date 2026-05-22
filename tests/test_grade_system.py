import pytest
from src.grade_system import GradeSystem, DuplicateGradeError, InvalidGradeError


class TestRegisterGrade:
    """REQ-1: Registrar nota entre 0.0 y 5.0"""

    def setup_method(self):
        self.system = GradeSystem()

    # TC01 - Positivo
    def test_register_valid_grade_stores_successfully(self):
        self.system.register_grade("Matemáticas", "2024-1", 3.5)
        assert ("Matemáticas", "2024-1") in self.system.grades

    # TC02 - Negativo
    def test_register_negative_grade_raises_invalid_error(self):
        with pytest.raises(InvalidGradeError):
            self.system.register_grade("Matemáticas", "2024-1", -1.0)

    # TC03 - Negativo
    def test_register_grade_above_maximum_raises_invalid_error(self):
        with pytest.raises(InvalidGradeError):
            self.system.register_grade("Matemáticas", "2024-1", 6.0)

    # TC04 - Borde
    def test_register_grade_at_minimum_boundary_zero_is_valid(self):
        self.system.register_grade("Matemáticas", "2024-1", 0.0)
        assert ("Matemáticas", "2024-1") in self.system.grades

    # TC05 - Borde
    def test_register_grade_at_maximum_boundary_five_is_valid(self):
        self.system.register_grade("Matemáticas", "2024-1", 5.0)
        assert ("Matemáticas", "2024-1") in self.system.grades

    def test_register_grade_just_below_minimum_raises_invalid_error(self):
        with pytest.raises(InvalidGradeError):
            self.system.register_grade("Matemáticas", "2024-1", -0.1)

    def test_register_grade_just_above_maximum_raises_invalid_error(self):
        with pytest.raises(InvalidGradeError):
            self.system.register_grade("Matemáticas", "2024-1", 5.1)

class TestPassingStatus:
    """REQ-2: Determinar aprobación (>=3.0 aprueba)"""

    def setup_method(self):
        self.system = GradeSystem()

    # TC06 - Positivo
    def test_grade_above_three_returns_passing(self):
        self.system.register_grade("Física", "2024-1", 3.5)
        assert self.system.is_passing("Física", "2024-1") is True

    # TC07 - Negativo
    def test_grade_below_three_returns_failing(self):
        self.system.register_grade("Física", "2024-1", 2.9)
        assert self.system.is_passing("Física", "2024-1") is False

    # TC08 - Borde
    def test_grade_exactly_three_returns_passing(self):
        self.system.register_grade("Física", "2024-1", 3.0)
        assert self.system.is_passing("Física", "2024-1") is True

    def test_grade_zero_returns_failing(self):
        self.system.register_grade("Física", "2024-1", 0.0)
        assert self.system.is_passing("Física", "2024-1") is False

    def test_grade_five_returns_passing(self):
        self.system.register_grade("Física", "2024-1", 5.0)
        assert self.system.is_passing("Física", "2024-1") is True

class TestAverage:
    """REQ-3: Calcular promedio de todas las notas"""

    def setup_method(self):
        self.system = GradeSystem()

    # TC09 - Positivo
    def test_average_with_no_grades_returns_zero(self):
        assert self.system.get_average() == 0.0

    # TC10 - Positivo
    def test_average_with_single_grade_returns_that_grade(self):
        self.system.register_grade("Matemáticas", "2024-1", 4.0)
        assert self.system.get_average() == 4.0

    # TC11 - Positivo
    def test_average_with_multiple_grades_returns_correct_average(self):
        self.system.register_grade("Matemáticas", "2024-1", 4.0)
        self.system.register_grade("Historia", "2024-1", 2.0)
        assert self.system.get_average() == 3.0

    def test_average_with_three_grades_returns_correct_average(self):
        self.system.register_grade("Matemáticas", "2024-1", 3.0)
        self.system.register_grade("Historia", "2024-1", 4.0)
        self.system.register_grade("Física", "2024-1", 5.0)
        assert self.system.get_average() == pytest.approx(4.0)

class TestDuplicateGrade:
    """REQ-4: No duplicar nota para misma materia en mismo semestre"""

    def setup_method(self):
        self.system = GradeSystem()

    # TC12 - Negativo
    def test_register_duplicate_grade_same_subject_same_semester_raises_error(self):
        self.system.register_grade("Matemáticas", "2024-1", 4.0)
        with pytest.raises(DuplicateGradeError):
            self.system.register_grade("Matemáticas", "2024-1", 3.0)

    # TC13 - Positivo
    def test_register_same_subject_different_semester_is_allowed(self):
        self.system.register_grade("Matemáticas", "2024-1", 4.0)
        self.system.register_grade("Matemáticas", "2024-2", 3.5)
        assert ("Matemáticas", "2024-2") in self.system.grades

    # TC14 - Positivo
    def test_register_different_subjects_same_semester_is_allowed(self):
        self.system.register_grade("Matemáticas", "2024-1", 4.0)
        self.system.register_grade("Historia", "2024-1", 3.5)
        assert ("Historia", "2024-1") in self.system.grades

    def test_duplicate_grade_error_message_is_descriptive(self):
        self.system.register_grade("Matemáticas", "2024-1", 4.0)
        with pytest.raises(DuplicateGradeError) as exc_info:
            self.system.register_grade("Matemáticas", "2024-1", 3.0)
        assert "Matemáticas" in str(exc_info.value)
        assert "2024-1" in str(exc_info.value)