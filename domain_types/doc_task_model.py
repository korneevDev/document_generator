from dataclasses import dataclass

from view_types.chapters import Chapter
from view_types.organization import Organization, Worker, Department
from view_types.program import Program
from view_types.skills import CommonProfSkills, Results
from view_types.subject import Subject


@dataclass
class DocumentTask:
    delete_marker : str

    organization: Organization
    workers: list[Worker]
    department: Department
    year: int
    profile: Program
    subject: Subject

    skills: CommonProfSkills
    results: Results

    chapters: list[Chapter]
