from dataclasses import dataclass


@dataclass
class Program:
    code: str
    name: str
    profile: str
    profile_code: int
    fgos_number: int
    fgos_start: str
