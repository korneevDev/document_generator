DROP TABLE IF EXISTS ThemeSkills;
DROP TABLE IF EXISTS Lesson;
DROP TABLE IF EXISTS Theme;
DROP TABLE IF EXISTS Chapter;
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS InventoryRoom;
DROP TABLE IF EXISTS InventorySubject;
DROP TABLE IF EXISTS ExamQuestion;
DROP TABLE IF EXISTS "Result";
DROP TABLE IF EXISTS Subject;
DROP TABLE IF EXISTS Room;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Skill;
DROP TABLE IF EXISTS ProgramOrganization;
DROP TABLE IF EXISTS "Program";
DROP TABLE IF EXISTS Fgos;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Worker;
DROP TABLE IF EXISTS Organization;

CREATE TABLE Organization(
	id SERIAL PRIMARY KEY,
	name VARCHAR(500),
	sity VARCHAR(50)
);

CREATE TABLE Worker(
	id SERIAL PRIMARY KEY,
	name VARCHAR(100),
	second_name VARCHAR(100),
	surname VARCHAR(100)
);

CREATE TABLE Department(
	id SERIAL PRIMARY KEY,
	name VARCHAR(200),
	head_id INT REFERENCES Worker(id),
	organization_id INT REFERENCES Organization(id),
	date_start DATE,
	date_end DATE
);

CREATE TABLE Fgos(
	id SERIAL PRIMARY KEY,
	number INT,
	date_start DATE,
	doc_link VARCHAR(500)
);

CREATE TABLE "Program"(
	id SERIAL PRIMARY KEY,
	"group" SMALLINT,
	"level" SMALLINT,
	"number" SMALLINT,
	name VARCHAR(200),
	profile_code SMALLINT,
	profile_name VARCHAR(100),
	fgos_id INT REFERENCES Fgos(id)
);

CREATE TABLE ProgramOrganization(
	id SERIAL PRIMARY KEY,
	program_id INT REFERENCES "Program"(id),
	organization INT REFERENCES Organization(id),
	date_start DATE,
	date_end DATE,
	is_active BOOL
);

CREATE TABLE Skill(
	id SERIAL PRIMARY KEY,
	"type" VARCHAR(10),
	code SMALLINT,
	name VARCHAR(200),
	root_skill INT REFERENCES Skill(id),
	program_id INT REFERENCES "Program"(id)
);

CREATE TABLE Inventory(
	id SERIAL PRIMARY KEY,
	name VARCHAR(200)
);

CREATE TABLE Room(
	id SERIAL PRIMARY KEY,
	name VARCHAR(200)
);

CREATE TABLE Subject(
	id SERIAL PRIMARY KEY,
	"type" VARCHAR(10),
	code VARCHAR(10),
	name VARCHAR(500),
	is_required BOOL,
	is_exam BOOL,
	exam_time INT,
	exam_cons_time INT,
	room_id INT REFERENCES Room(id),
	count_questions_in_test SMALLINT
);

CREATE TABLE "Result"(
	id SERIAL PRIMARY KEY,
	"type" VARCHAR(20),
	name VARCHAR(500),
	subject_id INT REFERENCES Subject(id)
);

CREATE TABLE ExamQuestion(
	id SERIAL PRIMARY KEY,
	subject_id INT REFERENCES Subject(id),
	"type" VARCHAR(20),
	"text" TEXT
);

CREATE TABLE InventoryRoom(
	id SERIAL PRIMARY KEY,
	invenory_id INT REFERENCES Inventory(id),
	room_id INT REFERENCES Room(id)
);

CREATE TABLE InventorySubject(
	id SERIAL PRIMARY KEY,
	invenory_id INT REFERENCES Inventory(id),
	subject_id INT REFERENCES Subject(id)
);

CREATE TABLE Book(
	id SERIAL PRIMARY KEY,
	subject_id INT REFERENCES Subject(id),
	"type" VARCHAR(10),
	"link" VARCHAR(500)
);

CREATE TABLE Chapter(
	id SERIAL PRIMARY KEY,
	subject_id INT REFERENCES Subject(id),
	name VARCHAR(100),
	semester SMALLINT
);

CREATE TABLE Theme(
	id SERIAL PRIMARY KEY,
	chapter_id INT REFERENCES Theme(id),
	name VARCHAR(500)
);

CREATE TABLE ThemeSkills(
	id SERIAL PRIMARY KEY,
	theme_id INT REFERENCES Theme(id),
	skill_id INT REFERENCES Skill(id)
);

CREATE TABLE Lesson(
	id SERIAL PRIMARY KEY,
	"type" VARCHAR(20),
	name VARCHAR(200),
	"hour" SMALLINT,
	"number" SMALLINT,
	theme_id INT REFERENCES Theme(id)
);

