from dataclasses import dataclass

from domain_types.chapters import Chapter
from domain_types.organization import Organization, Worker, Department
from domain_types.program import Program
from domain_types.skills import CommonProfSkills, Results
from domain_types.subject import Subject, SubjectYear


@dataclass
class DocumentTask:
    delete_marker : str

    organization: Organization
    workers: list[Worker]
    department: Department
    profile: Program
    subject: SubjectYear

    skills: CommonProfSkills
    results: Results

    chapters: list[Chapter]
