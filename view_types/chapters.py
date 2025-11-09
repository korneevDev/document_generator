from dataclasses import dataclass


@dataclass
class Lesson:
    name: str
    hour: int

@dataclass
class PracticeLesson(Lesson):
    number: int

@dataclass
class Theme:
    name: str
    lectures: list[Lesson]
    skills: list[str]

@dataclass
class PracticeTheme(Theme):
    practices: list[Lesson]

@dataclass
class SelfWorkTheme(Theme):
    self_works: list[Lesson]

@dataclass
class SelfWorkPracticeTheme(PracticeTheme, SelfWorkTheme):
    pass

@dataclass
class Chapter:
    name: str
    semester: int
    themes: list[Theme]