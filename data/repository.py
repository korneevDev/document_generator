import psycopg2

from domain_types.organization import Organization, Worker, Department
from domain_types.program import Program
from domain_types.skills import CommonProfSkills, ProfessionalSkills, Skill, Results
from domain_types.subject import Subject, Room, Books, ExamQuestions
from view_types.program_view_model import ProgramViewModel


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5433,
        user="postgres",
        password="root",
        database="doc_generator_db"
    )


def load_subjects() -> list[Subject]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""SELECT id, "type", code, name, is_required, room_id
                    FROM Subject""")
    rows_subject = cur.fetchall()

    subjects = []

    for row_subject in rows_subject:
        cur.execute("""SELECT r.name, i.name
                                FROM Room r 
                                    JOIN inventoryroom ir 
                                        ON r.id = ir.room_id
                                    JOIN inventory i 
                                        ON i.id = ir.inventory_id
                                WHERE r.id = %s""", [row_subject[5]])
        rows_room = cur.fetchall()
        room_name = ''
        inventory = []
        for row in rows_room:
            room_name = row[0]
            inventory.append(row[1])
        room = Room(room_name, inventory)

        cur.execute("""SELECT i.name
                FROM inventorysubject ir 
                    JOIN inventory i 
                        ON i.id = ir.inventory_id
                WHERE ir.subject_id=%s
        """, [row_subject[0]])

        subject_inventory = [i[0] for i in cur.fetchall()]

        cur.execute("""SELECT "type", "link"
                        FROM Book
                        WHERE subject_id = %s
        """, [row_subject[0]])
        rows_book = cur.fetchall()

        books = Books([], [], [])
        books_dictionary = {
            'main': books.main,
            'addition': books.addition,
            'electronic': books.electronic
        }

        for book in rows_book:
            books_dictionary[book[0]].append(book[1])

        cur.execute("""SELECT "type", text FROM ExamQuestion WHERE subject_id = %s""", [row_subject[0]])

        questions = ExamQuestions(2, [], [])
        questions_dict = {
            'theory': questions.theory,
            'practice': questions.practice
        }

        rows = cur.fetchall()

        for row in rows:
            questions_dict[row[0]].append(row[1])

        subjects.append(Subject(
            type=row_subject[1],
            code=row_subject[2],
            name=row_subject[3],
            is_required=row_subject[4],
            books=books,
            add_inventory=subject_inventory,
            room=room,
            exam_questions=questions
        ))

    conn.close()

    return subjects


def load_departments() -> list[Department]:
    con = get_connection()

    cur = con.cursor()

    cur.execute('''SELECT d.name, w.second_name, w.name, w.surname 
                    FROM Department d JOIN Worker w ON w.id = d.head_id''')

    rows = cur.fetchall()

    return [
        Department(
            row[0],
            Worker(
                row[1],
                row[2],
                row[3]
            )
        )
        for row in rows
    ]


def load_organizations() -> list[Organization]:
    con = get_connection()

    cur = con.cursor()

    cur.execute('''SELECT name, city 
                    FROM Organization''')

    rows = cur.fetchall()

    return [
        Organization(
            row[0],
            row[1]
        )
        for row in rows
    ]


def load_workers() -> list[Worker]:
    con = get_connection()

    cur = con.cursor()

    cur.execute('''SELECT name, second_name, surname 
                    FROM Worker''')

    rows = cur.fetchall()

    return [
        Worker(
            name=row[0],
            lastname=row[1],
            surname=row[2]
        )
        for row in rows
    ]


def load_programs() -> list[ProgramViewModel]:
    con = get_connection()

    cur = con.cursor()

    cur.execute('''SELECT CONCAT(p."group", '.', p."level", '.' , p."number"), 
                    p.name, f.number, f.date_start
                        FROM "Program" p 
                            JOIN Fgos f 
                        ON p.fgos_id = f.id''')

    rows = cur.fetchall()

    return [
        ProgramViewModel(
            row[0],
            row[1],
            row[2],
            row[3]
        )
        for row in rows
    ]


def save_fgos(program, skills, pdf_path):
    conn = get_connection()
    cursor = conn.cursor()

    program_id = save_fgos_program_data(cursor, program, pdf_path)
    save_skills(cursor, program_id, skills)

    conn.commit()
    cursor.close()
    conn.close()


def save_to_table_with_returning_id(cursor, data: dict[str], table_name):
    fields = [f'"{field}"' for field in data]
    query = f"""INSERT INTO {table_name} ({', '.join(fields)}) 
                    VALUES ({', '.join(['%s'] * len(fields))}) 
                    RETURNING id"""

    values = tuple(data.values())
    cursor.execute(query, values)
    return cursor.fetchone()[0]


def save_fgos_program_data(cursor, program: Program, link="https://fgos.ru"):
    fgos_data = program.get_fgos_data_to_db() | {'doc_link': link}
    fgos_id = save_to_table_with_returning_id(cursor, fgos_data, 'Fgos')

    program_data = program.get_program_data_to_db() | {'fgos_id': fgos_id}
    program_id = save_to_table_with_returning_id(cursor, program_data, '"Program"')

    return program_id


def save_skills(cursor, program_id, skills: CommonProfSkills):
    skills_data = skills.get_db_list(program_id, save_to_table_with_returning_id, cursor, 'Skill')
    print(skills_data)
    for skill_data in skills_data:
        save_to_table_with_returning_id(cursor, skill_data, 'Skill')


def load_skills_subject(subject: Subject) -> CommonProfSkills:
    con = get_connection()

    cur = con.cursor()

    cur.execute('''SELECT s."type", s.code, s.name, s.root_skill 
                    FROM Skill s JOIN SubjectSkills ss ON s.id = ss.skill_id 
                    JOIN Subject sss ON ss.subject_id = sss.id
                    WHERE sss.code = %s AND sss."type" = %s''',
                [subject.code, subject.type])

    rows = cur.fetchall()

    common_prof_skills = CommonProfSkills([], [])

    for row in rows:
        if row[0] == 'ВД':
            prof_skill = ProfessionalSkills(row[0], row[1], row[2], [])
            common_prof_skills.professional.append(prof_skill)

    for row in rows:
        if row[0] == 'ОК':
            common_prof_skills.common.append(Skill(row[0], row[1], row[2]))
        elif row[0] == 'ПК':
            for skill in common_prof_skills.professional:
                if skill.code == row[1].split('.')[0]:
                    skill.skills.append(Skill(row[0], row[1], row[2]))

    return common_prof_skills


def load_results_skill(subject, activity_code) -> Results:
    con = get_connection()

    cur = con.cursor()

    cur.execute('''SELECT r."type", r.name FROM "Result" r
                        JOIN Skill s ON s.id = r.skill_id
                        JOIN Subject sub ON sub.program_id = s.program_id  
		                    AND sub.code = %s AND sub."type" = %s
                    WHERE s.code = %s''',
                [subject.code, subject.type, activity_code[0]])

    rows = cur.fetchall()

    results = Results([], [])
    results_dict = {
        'skill': results.skill,
        'knowledge': results.knowledge
    }

    for row in rows:
        results_dict[row[0]].append(row[1])

    return results
