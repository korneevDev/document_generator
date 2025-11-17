from dataclasses import dataclass


@dataclass
class SkillView:
    code: str
    name: str

@dataclass
class ProfessionalSkillsView(SkillView):
    skills: list[SkillView]


@dataclass
class CommonProfSkillsView:
    common: list[SkillView]
    professional: ProfessionalSkillsView

@dataclass
class PersonalSkillsView(CommonProfSkillsView):
    personal: list[SkillView]

@dataclass
class AimPersonalSkillsView(PersonalSkillsView):
    aim: list[SkillView]


@dataclass
class ResultsView:
    skill: list[str]
    knowledge: list[str]
