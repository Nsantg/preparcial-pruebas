MIN_GRADE = 0.0
MAX_GRADE = 5.0
PASSING_GRADE = 3.0

class InvalidGradeError(Exception):
    pass


class DuplicateGradeError(Exception):
    pass


class GradeSystem:
    def __init__(self):
        self.grades: dict[tuple[str, str], float] = {}

    def register_grade(self, subject: str, semester: str, grade: float) -> None:
        """Registra una nota para una materia en un semestre dado."""
        if not (MIN_GRADE <= grade <= MAX_GRADE):
            raise InvalidGradeError(
                f"La nota {grade} no es válida. "
                f"Debe estar entre {MIN_GRADE} y {MAX_GRADE}."
            )
        if (subject, semester) in self.grades:
            raise DuplicateGradeError(
                f"Ya existe una nota para '{subject}' "
                f"en el semestre '{semester}'. "
                f"No se puede registrar una nota duplicada."
            )
        self.grades[(subject, semester)] = grade

    def is_passing(self, subject: str, semester: str) -> bool:
        """Retorna True si la nota de la materia en el semestre es >= PASSING_GRADE."""
        if (subject, semester) not in self.grades:
            raise ValueError(
                f"No hay nota registrada para {subject} en el semestre {semester}"
            )
        return self.grades[(subject, semester)] >= PASSING_GRADE

    def get_average(self) -> float:
        """Retorna el promedio de todas las notas. Retorna 0.0 si no hay notas."""
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)