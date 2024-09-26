CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(250) NOT NULL UNIQUE, 
    course_number INT CHECK (course_number > 0)
);

CREATE TABLE IF NOT EXISTS disciplines (
    id SERIAL PRIMARY KEY, 
    discipline_name VARCHAR(100) NOT NULL UNIQUE, 
    day_of_week VARCHAR(20) CHECK (day_of_week IN ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота')), 
    lesson_number INT CHECK (lesson_number > 0 AND lesson_number <= 6), 
    course_number INT CHECK (course_number > 0 AND course_number <= 6)
);

COPY students(id, name, course_number)
FROM '/docker-entrypoint-initdb.d/students.csv'
DELIMITER ';'
CSV HEADER;

