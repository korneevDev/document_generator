from dataclasses import dataclass, field
from datetime import date


@dataclass
class Program:
    code: str = field(init=False)
    group: str
    level : str
    number : str
    name: str
    fgos_number: int
    fgos_start: date
    profile: str | None = None
    profile_code: int | None = None

    def __post_init__(self):
        self.code = f'{self.group}.{self.level}.{self.number}'

    def get_fgos_data_to_db(self):
        return {'number': self.fgos_number, 'date_start': self.fgos_start}

    def get_program_data_to_db(self):
        return {
            'group': self.group,
            'level': self.level,
            'number': self.number,
            'name': self.name
        }