class InvalidGradeError(Exception):
    pass


class DuplicateGradeError(Exception):
    pass


class GradeSystem:
    def __init__(self):
        self.grades: dict[tuple[str, str], float] = {}

    def register_grade(self, subject: str, semester: str, grade: float) -> None:
        if grade < 0.0 or grade > 5.0:
            raise InvalidGradeError(
                f"Nota inválida: {grade}. Debe estar entre 0.0 y 5.0"
            )
        self.grades[(subject, semester)] = grade