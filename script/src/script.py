import psycopg2
import logging

logging.basicConfig(level=logging.INFO, filename="script/logs/py_log.log",filemode="w",
                    format="%(asctime)s.%(msecs)03d %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
def connect():
	try:
		conn = psycopg2.connect(
			database = "db",
			user = "user",
			password ="pass",
			port = "5432",
			host = "localhost"
		)
		logging.info("Connection with DB established successfully")
		cur = conn.cursor()
		return (cur, conn)
	except:
		logging.error("Error while connecting to DB")

# Функция для создания таблиц students и disciplines
def create_tables(cur, conn):
    if cur is not None and conn is not None:
        try:
            # Создание таблицы students
            cur.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY, 
                    name VARCHAR(100) NOT NULL, 
                    course_number INT CHECK (course_number > 0 AND course_number <= 6)
                );
            """)
            
            # Создание таблицы disciplines
            cur.execute("""
                CREATE TABLE IF NOT EXISTS disciplines (
                    id SERIAL PRIMARY KEY, 
                    discipline_name VARCHAR(100) NOT NULL, 
                    day_of_week VARCHAR(20) CHECK (day_of_week IN ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота')), 
                    lesson_number INT CHECK (lesson_number > 0 AND lesson_number <= 6), 
                    course_number INT CHECK (course_number > 0 AND course_number <= 6)
                );
            """)

            conn.commit()
            logging.info("Tables created successfully")
        except Exception as e:
            logging.error("Error while creating tables: %s", e)
            
# API функции
def get_student(student_id, cur):
    cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cur.fetchone()
    if student:
        logging.info(f"Student data: {student}")
        return student
    else:
        logging.warning("Student not found")
        return None

def get_discipline(course_number, cur):
    cur.execute("SELECT * FROM disciplines WHERE course_number = %s ORDER BY day_of_week, lesson_number", (course_number,))
    disciplines = cur.fetchall()
    if disciplines:
        logging.info(f"Disciplines for course {course_number}: {disciplines}")
        return disciplines
    else:
        logging.warning("No disciplines found")
        return None

def get_students_by_course(course_number, cur):
    cur.execute("SELECT * FROM students WHERE course_number = %s ORDER BY name", (course_number,))
    students = cur.fetchall()
    if students:
        logging.info(f"Students for course {course_number}: {students}")
        return students
    else:
        logging.warning("No students found")
        return None

def get_all_disciplines(cur):
    cur.execute("SELECT * FROM disciplines ORDER BY day_of_week, lesson_number")
    disciplines = cur.fetchall()
    logging.info("All disciplines: %s", disciplines)
    return disciplines

def add_student(name, course_number, cur, conn):
    cur.execute("INSERT INTO students (name, course_number) VALUES (%s, %s) RETURNING *", (name, course_number))
    student = cur.fetchone()
    conn.commit()
    logging.info(f"Added student: {student}")
    return student
def add_discipline(discipline_name, day_of_week, lesson_number, course_number, cur, conn):
    cur.execute("""
        INSERT INTO disciplines (discipline_name, day_of_week, lesson_number, course_number)
        VALUES (%s, %s, %s, %s)
    """, (discipline_name, day_of_week, lesson_number, course_number))
    conn.commit()
    logging.info(f"Added discipline: {discipline_name}, Day: {day_of_week}, Lesson: {lesson_number}, Course: {course_number}")

def delete_student(student_id, cur, conn):
    cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    logging.info(f"Deleted student with ID: {student_id}")

def delete_discipline(discipline_id, cur, conn):
    cur.execute("DELETE FROM disciplines WHERE id = %s", (discipline_id,))
    conn.commit()
    logging.info(f"Deleted discipline with ID: {discipline_id}")

# Пример использования функций:
cursor, conn = connect()

# Создание таблиц
create_tables(cursor, conn)

# Вызов команд API
get_student(1, cursor)
# get_discipline(2, cursor)
# get_students_by_course(3, cursor)
# get_all_disciplines(cursor)
# add_student('Ivan Ivanov', 1, cursor, conn)
# add_discipline('Mathematics', 'Понедельник', 1, 1, cursor, conn)
# delete_student(1, cursor, conn)
# delete_discipline(2, cursor, conn)