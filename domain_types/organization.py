from dataclasses import dataclass, field


@dataclass
class Worker:
    lastname: str
    name: str
    surname: str
    initials: str = field(init=False)

    def __post_init__(self):
        self.initials = f'{self.lastname} {self.name[:1]}.{self.surname[:1]}.'

    def __str__(self):
        return self.initials

@dataclass
class Department:
    name: str
    head: Worker

    def __str__(self):
        return self.name

@dataclass
class Organization:
    name: str
    city: str

    def __str__(self):
        return self.name