import itertools
from dataclasses import dataclass

from view_types.view_skill_type import CommonProfSkillsView, SkillView, ProfessionalSkillsView


@dataclass
class Results:
    skill: list[str]
    knowledge: list[str]


@dataclass
class Skill:
    type: str
    code: str
    name: str

    def get_db_view(self):
        return self.__dict__

    def get_group_number(self):
        return self.code.split('.')[0]

    def map_to_prof_skills(self, inner_skills):
        return ProfessionalSkills(self.type, self.code, self.name, inner_skills)

    def get_value_from_skill_code(self, search_dict):
        return search_dict[self.code]

    def __eq__(self, other):
        return f'{self.type}.{self.code}' == f'{other.type}.{other.code}'

    def __hash__(self):
        return self.type.__hash__() + self.code.__hash__()

    def __str__(self):
        return f'{self.type} {self.code}'

    def map_to_view(self):
        return SkillView(f'{self.type} {self.code}', self.name)


@dataclass
class ProfessionalSkills(Skill):
    skills: list[Skill]
    results: Results = None

    def get_db_list(self, program_id: int, func_get_lesson_id, cursor, table_name):
        activity_id = func_get_lesson_id(
            cursor=cursor, table_name=table_name, data={
                'type': self.type, 'code': self.code,
                'name': self.name, 'program_id': program_id,
                'root_skill': None
            }
        )

        return [
            skill.get_db_view() | {
                'root_skill': activity_id,
                'program_id': program_id
            }
            for skill in self.skills
        ]

    def to_str_list(self):
        return [str(Skill(self.type, self.code, self.name))] + [str(skill) for skill in self.skills]

    def map_to_view(self):
        return ProfessionalSkillsView(self.code, self.name, [it.map_to_view() for it in  self.skills])


@dataclass
class CommonProfSkills:
    common: list[Skill]
    professional: list[ProfessionalSkills]

    def get_activity_code(self):
        return [skill.code for skill in self.professional]

    def get_db_list(self, program_id: int, func_get_activity_id, cursor, table_name):
        result = []

        for skill in self.professional:
            result += skill.get_db_list(program_id, func_get_activity_id, cursor, table_name)

        return result + [
            skill.get_db_view() | {
                'program_id': program_id
            }
            for skill in self.common
        ]

    def to_str_list(self):
        return [str(com) for com in self.common] + [str(prof) for prof in self.professional]

    def map_to_view(self):
        return CommonProfSkillsView(common=[s.map_to_view() for s in self.common], professional=self.professional[0].map_to_view())

    def map_to_list_view(self):
        com = [str(it) for it in self.common]
        prof = []

        for it in self.professional:
            prof.extend(it.to_str_list())
        return com + prof


@dataclass
class PersonalSkills(CommonProfSkills):
    personal: list[Skill]

    def get_db_list(self, program_id: int, func_get_activity_id, cursor, table_name):
        return super().get_db_list(program_id, func_get_activity_id, cursor, table_name) + \
            [
                skill.get_db_view() | {
                    'program_id': program_id
                }
                for skill in self.personal
            ]


@dataclass
class AimPersonalSkills(PersonalSkills):
    aim: list[Skill]

    def get_db_list(self, program_id: int, func_get_activity_id, cursor, table_name):
        return super().get_db_list(program_id, func_get_activity_id, cursor, table_name) + \
            [
                skill.get_db_view() | {
                    'program_id': program_id
                }
                for skill in self.aim
            ]
