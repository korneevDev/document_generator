from dataclasses import dataclass, field


@dataclass
class Worker:
    lastname: str
    name: str
    surname: str
    initials: str = field(init=False)

    def __post_init__(self):
        self.initials = f'{self.lastname} {self.name[:1]}.{self.surname[:1]}.'


@dataclass
class Department:
    name: str
    head: Worker

@dataclass
class Organization:
    name: str
    city: str