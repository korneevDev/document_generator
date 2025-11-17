from dataclasses import dataclass


@dataclass
class Room:
    name: str
    inventory: list[str]

@dataclass
class Books:
    main: list[str]
    addition: list[str]
    electronic: list[str]

@dataclass
class ExamQuestions:
    count: int
    theory: list[str]
    practice: list[str]

@dataclass
class Subject:
    code: str
    name: str
    is_required: bool
    is_exam: bool
    exam_time: int
    exam_cons_time: int

    room: Room
    add_inventory: list[str]

    books: Books

    exam_questions: ExamQuestions

@dataclass
class SubjectWithHours(Subject):
    total_hours : int
    total_hours_lectures : int
    total_hours_practices : int
    total_hours_self_works : int
