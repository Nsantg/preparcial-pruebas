MIN_GRADE: float = 0.0
MAX_GRADE: float = 5.0
PASSING_GRADE: float = 3.0


class InvalidGradeError(Exception):
    pass


class DuplicateGradeError(Exception):
    pass


class GradeSystem:
    def __init__(self) -> None:
        self.grades: dict[tuple[str, str], float] = {}

    def _is_duplicate(self, subject: str, semester: str) -> bool:
        return (subject, semester) in self.grades

    def _is_valid_grade(self, grade: float) -> bool:
        return MIN_GRADE <= grade <= MAX_GRADE

    def register_grade(self, subject: str, semester: str, grade: float) -> None:
        if not self._is_valid_grade(grade):
            raise InvalidGradeError(
                f"La nota {grade} no es válida. Debe estar entre {MIN_GRADE} y {MAX_GRADE}."
            )
        if self._is_duplicate(subject, semester):
            raise DuplicateGradeError(
                f"Ya existe una nota para '{subject}' en el semestre '{semester}'."
            )
        self.grades[(subject, semester)] = grade

    def is_passing(self, subject: str, semester: str) -> bool:
        if (subject, semester) not in self.grades:
            raise ValueError(
                f"No hay nota registrada para '{subject}' en el semestre '{semester}'."
            )
        return self.grades[(subject, semester)] >= PASSING_GRADE

    def get_average(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)