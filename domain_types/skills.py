from dataclasses import dataclass


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


@dataclass
class ProfessionalSkills(Skill):
    skills: list[Skill]

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


@dataclass
class CommonProfSkills:
    common: list[Skill]
    professional: list[ProfessionalSkills]

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


@dataclass
class Results:
    skill: list[str]
    knowledge: list[str]
