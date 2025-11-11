INSERT INTO Department (name, head_id, organization_id, date_start, date_end)
SELECT
    dept_name AS name,
    w.id AS head_id,
    org.id AS organisation_id,
    '2025-02-20' AS date_start,
    '2025-10-01' AS date_end
FROM (VALUES
    ('информационных технологий и программирования', 'Комышан', 'Петр'),
    ('разработки веб приложений и информационной безопасности', 'Первушин', 'Владимир'),
	('социально-экономических дисциплин', 'Вологина', 'Ольга'),
    ('общеобразовательных дисциплин', 'Пашкевич', 'Галина'),
    ('графического дизайна и рекламы', 'Журба', 'Ольга'),
    ('социальных и правовых дисциплин и логистики', 'Мартанова', 'Кристина')
) AS dept_data(dept_name, second_name, name)
JOIN Worker w ON w.name = dept_data.name
              AND w.second_name = dept_data.second_name
JOIN Organization org ON org.name LIKE '%КЭСИ%';

INSERT INTO Department (name, head_id, organization_id, date_start, date_end)
SELECT
    dept_name AS name,
    w.id AS head_id,
    org.id AS organisation_id,
    '2025-02-20' AS date_start,
    '2025-10-01' AS date_end
FROM (VALUES
    ('информационных технологий и информационной безопасности', 'Комышан', 'Петр'),
    ('программирования и веб-разработки', 'Первушин', 'Владимир'),
	('социально-экономических дисциплин', 'Яхимович', 'Светлана'),
    ('общеобразовательных дисциплин', 'Пашкевич', 'Галина'),
    ('графического дизайна и рекламы', 'Журба', 'Ольга'),
    ('правовых дисциплин и логистики', 'Родионова', 'Людмила')
) AS dept_data(dept_name, second_name, name)
JOIN Worker w ON w.name = dept_data.name
              AND w.second_name = dept_data.second_name
JOIN Organization org ON org.name LIKE '%КЭСИ%';