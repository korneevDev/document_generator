from dataclasses import dataclass


@dataclass
class ProgramViewModel:
    """
    Образовательная программа

    Attributes:
        group: Укрупнённая группа
        level: Уровень образования
        number: Номер направления
    """

    code: str
    name: str
    fgos_number: int
    fgos_start: str

    def __str__(self):
        return f'{self.code} {self.name}'