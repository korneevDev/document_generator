from dataclasses import dataclass


@dataclass
class Skill:
    code: str
    name: str

@dataclass
class ProfessionalSkills(Skill):
    skills: list[Skill]

@dataclass
class CommonProfSkills:
    common: list[Skill]
    professional: ProfessionalSkills

@dataclass
class PersonalSkills(CommonProfSkills):
    personal: list[Skill]

@dataclass
class AimPersonalSkills(PersonalSkills):
    aim: list[Skill]

@dataclass
class Results:
    skill: list[str]
    knowledge: list[str]