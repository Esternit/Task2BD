-- Создаем таблицу students
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(250) NOT NULL, 
    course_number INT
);
-- Импортируем данные из CSV-файла
COPY students(id, name, course_number)
FROM '/docker-entrypoint-initdb.d/students.csv'
DELIMITER ';'
CSV HEADER;

