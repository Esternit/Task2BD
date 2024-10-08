import psycopg2
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s.%(msecs)03d %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
def connect():
	try:
		conn = psycopg2.connect(
			database = "db",
			user = "user",
			password ="pass",
			port = "5432",
			host = "dbpg-mtg"
		)
		logging.info("Connection with DB established successfully")
		cur = conn.cursor()
		return (cur, conn)
	except Exception as e:
		logging.error("Error while connecting to DB : %s", e)

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
    try:
        cur.execute("""INSERT INTO students (name, course_number) VALUES (%s, %s) 
        ON CONFLICT (name)
        DO UPDATE SET course_number = EXCLUDED.course_number
        RETURNING *;
        """, (name, course_number))
        student = cur.fetchone()
        conn.commit()  
        logging.info(f"Added student: {student}")
        return student
    except Exception as e:

        logging.error(f"Error adding student: {e}")
        

        conn.rollback()

        try:

            # Так как мы загружаем информацию из CSV-файла, где указаны id, то надо ресетнуть его здесь
            cur.execute("SELECT MAX(id) FROM students")
            max_id = cur.fetchone()[0]
            if max_id is None:
                max_id = 0  
            cur.execute("SELECT setval(pg_get_serial_sequence('students', 'id'), %s)", (max_id,))
            conn.commit()  
            
            logging.info(f"Sequence updated to {max_id}")

            cur.execute("""INSERT INTO students (name, course_number) VALUES (%s, %s) 
            ON CONFLICT (name)
            DO UPDATE SET course_number = EXCLUDED.course_number
            RETURNING *;
            """, (name, course_number))
            student = cur.fetchone()
            conn.commit() 
            logging.info(f"Added student after sequence update: {student}")
            return student
        except Exception as seq_e:
            conn.rollback()
            logging.error(f"Failed to update sequence or add student: {seq_e}")
            return None


def add_discipline(discipline_name, day_of_week, lesson_number, course_number, cur, conn):
    try:
        cur.execute("""
            INSERT INTO disciplines (discipline_name, day_of_week, lesson_number, course_number)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (discipline_name)
            DO UPDATE SET day_of_week = EXCLUDED.day_of_week, lesson_number = EXCLUDED.lesson_number, course_number = EXCLUDED.course_number
            RETURNING *;
        """, (discipline_name, day_of_week, lesson_number, course_number))
        discipline = cur.fetchone()
        conn.commit()
        logging.info(f"Added discipline: {discipline_name}, Day: {day_of_week}, Lesson: {lesson_number}, Course: {course_number}")
        return discipline
    except Exception as e:
        conn.rollback()
        logging.error(f"Error adding discipline: {e}")
        return None

def delete_student(student_id, cur, conn):
    cur.execute("DELETE FROM students WHERE id = %s RETURNING *", (student_id,))
    student = cur.fetchone()
    conn.commit()
    logging.info(f"Deleted student with ID: {student_id}")
    return student

def delete_discipline(discipline_id, cur, conn):
    cur.execute("DELETE FROM disciplines WHERE id = %s RETURNING *", (discipline_id,))
    discipline = cur.fetchone()
    conn.commit()
    logging.info(f"Deleted discipline with ID: {discipline_id}")
    return discipline

#  Пример использования функций:
# cursor, conn = connect()

#  Создание таблиц
# create_tables(cursor, conn)

#  Вызов команд API
# get_student(1, cursor)
# get_discipline(2, cursor)
# get_students_by_course(3, cursor)
# get_all_disciplines(cursor)
# add_student('Ivan Ivanov', 1, cursor, conn)
# add_discipline('Mathematics', 'Понедельник', 1, 1, cursor, conn)
# delete_student(1, cursor, conn)
# delete_discipline(2, cursor, conn)