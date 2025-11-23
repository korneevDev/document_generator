from dataclasses import dataclass

from domain_types.organization import Organization, Worker, Department
from domain_types.subject import SubjectYear
from view_types.program_view_model import ProgramViewModel
from view_types.view_skill_type import CommonProfSkillsView, ResultsView


@dataclass
class DocumentTaskView:
    delete_marker : str

    organization: Organization
    workers: list[Worker]
    department: Department
    profile: ProgramViewModel
    subject: SubjectYear

    skills: CommonProfSkillsView
    results: ResultsView

