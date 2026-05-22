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