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
        if not (MIN_GRADE <= grade <= MAX_GRADE):
            raise InvalidGradeError(
                f"La nota {grade} no es válida. "
                f"Debe estar entre {MIN_GRADE} y {MAX_GRADE}."
            )
        self.grades[(subject, semester)] = grade