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

cursor, conn = connect()

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
        finally:
            cur.close()
            conn.close()
            
create_tables(cursor, conn)