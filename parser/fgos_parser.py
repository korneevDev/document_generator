import re
from collections import defaultdict
from dataclasses import dataclass

import pdfplumber
from datetime import datetime

from data import repository
from domain_types.program import Program
from domain_types.skills import Skill, CommonProfSkills, ProfessionalSkills

@dataclass
class PdfParser:
    pdf_path: str
    text: str = ''

    def extract_text_from_pdf(self) -> str:
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        match_doc = re.search(r"(fgos\.ru\n[0-9]*[0-9]\.[0-9]*[0-9]\.[0-9][0-9][0-9][0-9]\n)", text)
        text = text.replace(match_doc.group(0), '')
        self.text = text

    def extract_fgos_info(self):
        """
        Извлекает номер приказа, дату и направление
        """
        # дата и номер
        match_doc = re.search(r"от\s+(\d{1,2}\s+\S+\s+\d{4})\s+г\.\s*№\s*([0-9]+)", self.text)
        date_start = None
        number = None
        if match_doc:
            date_str = match_doc.group(1)
            try:
                date_start = datetime.strptime(date_str, "%d %B %Y").date()
            except ValueError:
                # Если месяц не на русском, можно использовать ruparser (или вручную)
                months = {
                    "января": 1, "февраля": 2, "марта": 3, "апреля": 4, "мая": 5,
                    "июня": 6, "июля": 7, "августа": 8, "сентября": 9, "октября": 10,
                    "ноября": 11, "декабря": 12
                }
                parts = date_str.split()
                if len(parts) == 3 and parts[1].lower() in months:
                    date_start = datetime(int(parts[2]), months[parts[1].lower()], int(parts[0])).date()
            number = match_doc.group(2)

        # направление
        match_dir = re.search(r"(\d{2}\.\d{2}\.\d{2})\s+([А-ЯЁа-яё\s\-]+)\n(В соответствии)", self.text)

        if not match_dir:
            raise ValueError(f'Не удалось получить данные направления из документа. Проверьте текст')

        direction = match_dir.group(1)

        group, level, direction_number = direction.split('.')

        direction_name = match_dir.group(2).strip().capitalize().replace('\n', ' ')

        return Program(group, level, direction_number, direction_name, number, date_start)

    def extract_activities(self, activities_nums: str):
        """
        Извлекает виды деятельности (ВД)
        """
        pattern = rf"[0-9]\.[0-9]\.([{activities_nums}])\. ([а-яА-Я \-\(\)\n,]*)(\.|:)"
        matches = re.findall(pattern, self.text)
        result = set()
        for match in matches:
            result.add(Skill('ВД', match[0], match[1]))

        return result

    def extract_competencies(self, prefix="ОК"):
        """
        Извлекает компетенции (ОК или ПК)
        """
        pattern = rf"{prefix}\s*[0-9.]+\.[а-яёА-ЯЁ ,\-\(\)\n]*\."
        matches = re.findall(pattern, self.text, flags=re.DOTALL)
        results = set()
        for m in matches:
            code_match = re.match(rf"({prefix} [0-9.]* )", m)
            if code_match:
                code = code_match.group(1).replace(". ", "").replace(prefix, '').strip()
                desc = m.replace(code_match.group(0), "").strip().replace('. ', '', 1).replace('\n', ' ')
                desc = re.sub('\\(.*от.*№.*\\).*', '', desc).strip()
                results.add(Skill(prefix, code, desc))

        return list(results)

    def parse_skills(self):

        ok_list = self.extract_competencies('ОК')

        pk_list = self.extract_competencies('ПК')

        pk_dict = defaultdict(list)

        for pk in pk_list:
            pk_dict[pk.get_group_number()].append(pk)

        activities_nums = ''.join(pk_dict.keys())
        activities_list = self.extract_activities(activities_nums)

        prof_list = []

        for activity in activities_list:
            prof_list.append(
                activity.map_to_prof_skills(
                    activity.get_value_from_skill_code(pk_dict)
                )
            )

        return CommonProfSkills(ok_list, prof_list)

def parse_fgos(pdf_path):
    parser = PdfParser(pdf_path)

    parser.extract_text_from_pdf()

    program = parser.extract_fgos_info()
    skills = parser.parse_skills()

    repository.save_fgos(program, skills, pdf_path)


if __name__ == "__main__":
    pdf_path = "../static/fgos_docs/09_02_07.pdf"
    parse_fgos(pdf_path)

    print("✅ Данные успешно сохранены в базу")
