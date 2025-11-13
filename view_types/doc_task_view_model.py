from dataclasses import dataclass

from domain_types.chapters import Chapter
from domain_types.organization import Organization, Worker, Department
from domain_types.subject import Subject
from view_types.program_view_model import ProgramViewModel
from view_types.view_skill_type import CommonProfSkillsView, ResultsView


@dataclass
class DocumentTaskView:
    delete_marker : str

    organization: Organization
    workers: list[Worker]
    department: Department
    year: int
    profile: ProgramViewModel
    subject: Subject

    skills: CommonProfSkillsView
    results: ResultsView

    chapters: list[Chapter]
