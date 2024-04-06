import asyncio
import datetime

import aiomysql
import os
from dotenv import load_dotenv
load_dotenv()
loop = asyncio.get_event_loop()
async def connection(loop, start=False):
    try:
        # global conn
        conn = await aiomysql.connect(
            host=os.getenv('MSQL_HOST'),
            user=os.getenv('MSQL_USER'),
            password=os.getenv('MSQL_PASSWORD'),
            db=os.getenv('MSQL_DB'),
            loop=loop,
            charset='utf8mb4',
            autocommit=True
        )
        if start:
            print('Connect to MYSQL DB succesfull!')
            conn.close()
        return conn
    except Exception as er:
        print('Error in connection to MYSQL DB: ', er)


async def user_exists(user_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT id FROM teachers WHERE user_id = %s', user_id)
        await con.commit()
        if cur.rowcount > 0:
            return True
        else:
            await cur.execute('SELECT id FROM students WHERE user_id = %s', user_id)
            if cur.rowcount > 0:
                return True
            else:
                return False

async def get_teacher_info(user_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT * FROM teachers WHERE user_id = %s', user_id)
        await con.commit()
        if cur.rowcount > 0:
            teacher_info = await cur.fetchall()
            result_info = {
                'user_id': teacher_info[0][1],
                'name': teacher_info[0][2],
                'subject': teacher_info[0][3],
            }
            return result_info
        else:
            return False


async def get_student_info(user_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT * FROM students WHERE user_id = %s', user_id)
        await con.commit()
        if cur.rowcount > 0:
            student_info = await cur.fetchall()
            result_info = {
                'user_id': student_info[0][1],
                'name': student_info[0][2],
                'subject': student_info[0][3],
            }
            return result_info
        else:
            return False


async def add_new_teacher(teacher_id, fio_teacher, subject):
    current_datetime = datetime.datetime.now()
    formatted_current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('INSERT INTO `teachers`(`user_id`, `name`, `subject`, `registration_date`) VALUES(%s, %s, %s, %s)', (teacher_id, fio_teacher, subject, formatted_current_datetime))
        await con.commit()


async def get_teachers():
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT * FROM teachers')
        await con.commit()
        if cur.rowcount > 0:
            teachers_info = await cur.fetchall()
            return teachers_info
        else:
            return False


async def get_students(teacher_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT * FROM `students` JOIN teachers ON students.teacher_id = teachers.id WHERE teachers.user_id = %s;', teacher_id)
        await con.commit()
        if cur.rowcount > 0:
            students_info = await cur.fetchall()
            return students_info
        else:
            return False


async def get_teacher_info_by_id(teacher_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT * FROM teachers WHERE user_id = %s', teacher_id)
        await con.commit()
        teacher_info = await cur.fetchone()
        return teacher_info


async def get_student_info_by_id(student_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT * FROM students JOIN teachers ON students.teacher_id = teachers.id WHERE students.user_id = %s', student_id)
        await con.commit()
        student_info = await cur.fetchone()
        return student_info

async def add_new_student(info_student):
    print(info_student["user_id"])
    student_id = info_student["user_id"]
    name = info_student["name"]
    subject = info_student["subject"]
    now_date = datetime.datetime.now()
    registration_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
    class_student = info_student["class_student"]
    purpose = info_student["purpose"]
    price = info_student["price"]
    transfer = f'{info_student["transfer"] if info_student["transfer"] is not None else "None"}'
    phone = f'{info_student["phone"] if info_student["phone"] is not None else "None"}'
    platform = f'{info_student["platform"] if info_student["platform"] is not None else "None"}'
    platform_nick = f'{info_student["platform_nick"] if info_student["platform_nick"] is not None else "None"}'
    timezone = info_student["timezone"]
    teacher_id = info_student["teacher_id"]

    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT id FROM students WHERE user_id = %s', student_id)
        await con.commit()
        if cur.rowcount > 0:
            return False

        await cur.execute('SELECT id FROM teachers WHERE user_id = %s', teacher_id)
        await con.commit()
        teacher_id = await cur.fetchone()
        await cur.execute('INSERT INTO `students`(`user_id`, `name`, `subject`, `registration_date`, `class`, `purpose`, `price`, `transfer`, `phone`, `platform`, `platform_nick`, `timezone`, `teacher_id`) '
                          'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (student_id, name, subject, registration_date, class_student, purpose, price, transfer, phone, platform, platform_nick, timezone, teacher_id))
        await con.commit()
        return True


async def generate_lessons_for_weekday(teacher_id, student_id, week_day, lesson_time):
    con = await connection(loop)
    lesson_hour = int((lesson_time.split(':'))[0])
    lesson_minute = int((lesson_time.split(':'))[1])

    current_date = datetime.datetime.now()
    current_year = current_date.year
    schedule_time = ''
    async with con.cursor() as cur:
        await cur.execute("SELECT id, price, teacher_id FROM students WHERE user_id = %s", student_id)
        await con.commit()
        if cur.rowcount > 0:
            student_info = await cur.fetchone()
            student_id = student_info[0]
            price = student_info[1]
            teacher_id = student_info[2]

    async with con.cursor() as cur:
        while current_date.year == current_year:
            if current_date.weekday() == week_day:
                schedule_time = (current_date.replace(hour=lesson_hour, minute=lesson_minute, second=0, microsecond=0)).strftime('%Y-%m-%d %H:%M:%S')

                await cur.execute("INSERT INTO lessons(`teacher_id`, `student_id`, `lesson_date`, `price`) VALUES (%s,%s,%s,%s)", (teacher_id, student_id, schedule_time, price))
                await con.commit()
            current_date += datetime.timedelta(days=1)


    ################# На месяц
    # while current_date.month == datetime.datetime.now().month:
    #     if current_date.weekday() == week_day:
    #         schedule_time = (
    #             current_date.replace(hour=lesson_hour, minute=lesson_minute, second=0, microsecond=0)).strftime(
    #             '%Y-%m-%d %H:%M:%S')
    #
    #         await cur.execute(
    #             "INSERT INTO lessons(`teacher_id`, `student_id`, `lesson_date`, `price`) VALUES (%s,%s,%s,%s)",
    #             (teacher_id, student_id, schedule_time, price))
    #         await con.commit()
    #     current_date += datetime.timedelta(days=1)

    ################### До конца года
    # con = await connection(loop)
    # lesson_hour = int((lesson_time.split(':'))[0])
    # lesson_minute = int((lesson_time.split(':'))[1])
    #
    # current_date = datetime.datetime.now()
    # current_year = current_date.year
    #
    # while current_date.year == current_year:
    #     if current_date.weekday() == week_day:
    #         schedule_time = current_date.replace(hour=lesson_hour, minute=lesson_minute, second=0, microsecond=0)
    #         print(schedule_time)
    #     current_date += datetime.timedelta(days=1)


async def get_lesson_dates_current_student(student_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("SELECT l.lesson_date FROM lessons AS l JOIN students AS s ON l.student_id = s.id WHERE s.user_id = %s", student_id)
        await con.commit()
        if cur.rowcount > 0:
            lesson_dates = await cur.fetchall()
            return lesson_dates
        else:
            return False


async def get_lessons_current_date(teacher_id, current_date):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("SELECT s.user_id, s.name, l.lesson_date, l.price, l.status "
                          "FROM lessons AS l "
                          "JOIN teachers AS t ON l.teacher_id = t.id "
                          "JOIN students AS s ON l.student_id = s.id "
                          "WHERE DATE(lesson_date) = %s AND t.user_id = %s "
                          "ORDER BY TIME(lesson_date) ASC", (current_date, teacher_id))
        await con.commit()

        if cur.rowcount > 0:
            lessons_info = await cur.fetchall()
            return lessons_info
        else:
            return False


async def get_lessons_week(teacher_id, start_date, end_date):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("SELECT s.user_id, s.name, l.lesson_date, l.price "
                          "FROM lessons AS l "
                          "JOIN teachers AS t ON l.teacher_id = t.id "
                          "JOIN students AS s ON l.student_id = s.id "
                          "WHERE DATE(lesson_date) BETWEEN %s AND %s AND t.user_id = %s "
                          "ORDER BY DATE(lesson_date), TIME(lesson_date) ASC",
                          (start_date, end_date, teacher_id))
        await con.commit()

        if cur.rowcount > 0:
            lessons_info = await cur.fetchall()
            return lessons_info
        else:
            return False


async def check_lesson_exists(student_id, teacher_id, week_day, lesson_time):


    # 1 - Воскресенье,  а по коду 6 - Воскресенье, поэтому форматируем
    if week_day == 0:
        week_day = 2
    elif week_day == 1:
        week_day = 3
    elif week_day == 2:
        week_day = 4
    elif week_day == 3:
        week_day = 5
    elif week_day == 4:
        week_day = 6
    elif week_day == 5:
        week_day = 7
    elif week_day == 6:
        week_day = 1

    lesson_time = f'{lesson_time}:00'

    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("SELECT l.id FROM lessons AS l JOIN students AS s ON l.student_id = s.id JOIN teachers AS t ON l.teacher_id = t.id "
                          "WHERE DAYOFWEEK(lesson_date) = %s AND TIME(lesson_date) = %s AND s.user_id = %s AND t.user_id = %s;", (week_day, lesson_time, student_id, teacher_id))
        await con.commit()
        if cur.rowcount > 0:
            return True
        else:
            return False
        
# Находит уроки у другого ученика на тоже время
async def check_lesson_exists_other_student(teacher_id, week_day, lesson_time):


    # 1 - Воскресенье,  а по коду 6 - Воскресенье, поэтому форматируем
    if week_day == 0:
        week_day = 2
    elif week_day == 1:
        week_day = 3
    elif week_day == 2:
        week_day = 4
    elif week_day == 3:
        week_day = 5
    elif week_day == 4:
        week_day = 6
    elif week_day == 5:
        week_day = 7
    elif week_day == 6:
        week_day = 1

    lesson_time = f'{lesson_time}:00'

    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("SELECT l.id FROM lessons AS l JOIN teachers AS t ON l.teacher_id = t.id "
                          "WHERE DAYOFWEEK(lesson_date) = %s AND TIME(lesson_date) = %s AND t.user_id = %s;", (week_day, lesson_time, teacher_id))
        await con.commit()
        if cur.rowcount > 0:
            return True
        else:
            return False



#################################### функции для изменения информации об ученике ############################################################

async def change_student_id(student_id, new_student_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("UPDATE `students` SET `user_id`= %s WHERE user_id = %s", (new_student_id, student_id))
        await con.commit()


async def change_student_name(student_id, new_student_name):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("UPDATE `students` SET `name`= %s WHERE user_id = %s", (new_student_name, student_id))
        await con.commit()


async def change_student_subject(student_id, new_subject):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("UPDATE `students` SET `subject`= %s WHERE user_id = %s", (new_subject, student_id))
        await con.commit()


async def change_student_class(student_id, new_class_student):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("UPDATE `students` SET `class`= %s WHERE user_id = %s", (new_class_student, student_id))
        await con.commit()


async def change_student_purpose(student_id, new_purpose):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("UPDATE `students` SET `purpose`= %s WHERE user_id = %s", (new_purpose, student_id))
        await con.commit()


async def change_student_price(student_id, new_price):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("UPDATE `students` SET `price`= %s WHERE user_id = %s", (new_price, student_id))
        await con.commit()


async def change_student_transfer(student_id, new_transfer):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("UPDATE `students` SET `transfer`= %s WHERE user_id = %s", (new_transfer, student_id))
        await con.commit()

async def change_student_phone(student_id, new_phone):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("UPDATE `students` SET `phone`= %s WHERE user_id = %s", (new_phone, student_id))
        await con.commit()

async def change_student_platform(student_id, new_platform):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("UPDATE `students` SET `platform`= %s WHERE user_id = %s", (new_platform, student_id))
        await con.commit()



async def change_student_nick(student_id, new_nick):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("UPDATE `students` SET `platform_nick`= %s WHERE user_id = %s", (new_nick, student_id))
        await con.commit()


async def change_student_timezone(student_id, new_timezone):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("UPDATE `students` SET `timezone`= %s WHERE user_id = %s", (new_timezone, student_id))
        await con.commit()

async def get_count_active_students_for_teacher(id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("SELECT COUNT(id) FROM students WHERE teacher_id = %s AND archiv = 0", id)
        await con.commit()

        if cur.rowcount > 0:
            count_students = await cur.fetchone()
            return count_students[0]
        else:
            return False
        

async def get_count_all_students_for_teacher(id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("SELECT COUNT(id) FROM students WHERE teacher_id = %s", id)
        await con.commit()
        if cur.rowcount > 0:
            count_students_all = await cur.fetchone()
            return count_students_all[0]
        else:
            return False

#############################################################################################################################################
        


async def get_mounth_price_for_teacher(id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("SELECT SUM(price) AS total_price \
                            FROM lessons \
                            WHERE lesson_date >= DATE_FORMAT(NOW(), '%%Y-%%m-01') \
                            AND lesson_date < DATE_ADD(DATE_FORMAT(NOW(), '%%Y-%%m-01'), INTERVAL 1 MONTH) \
                            AND teacher_id = %s", id)
        await con.commit()

        if cur.rowcount > 0:
            mounth_price = await cur.fetchone()
            return mounth_price[0]
        else:
            return False
        

async def get_count_lessons_for_teacher(id, status):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("SELECT COUNT(id) FROM lessons WHERE status = %s AND teacher_id = %s", (status, id))
        await con.commit()

        if cur.rowcount > 0:
            count_success_lessons = await cur.fetchone()
            return count_success_lessons[0]
        else:
            return False

        

async def get_lessons_current_date_and_time(current_datetime):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("SELECT l.id AS lesson_id, l.price AS lesson_price, l.lesson_date, "
                          "t.user_id AS teacher_tg_id, t.name AS teacher_name, "
                          "s.user_id AS student_tg_id, s.name AS student_name, s.subject AS student_subject, s.class AS student_class, s.purpose AS student_purpose, s.platform AS student_platform, s.platform_nick AS student_p_nick, "
                          "l.status AS lesson_status "  
                          "FROM lessons AS l JOIN teachers AS t ON l.teacher_id = t.id JOIN students AS s ON l.student_id = s.id "
                          "WHERE l.lesson_date = %s AND l.status <> 5", current_datetime)
        await con.commit()
        if cur.rowcount > 0:
            lessons_info = await cur.fetchall()
            return lessons_info
        else:
            return False


async def change_lesson_status(lesson_id, new_status):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("UPDATE `lessons` SET `status` = %s WHERE id = %s", (new_status, lesson_id))
        await con.commit()


async def get_teacher_settings_info(teacher_tg_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute("SELECT st_timezone, st_notif, st_nalog, st_autozapoln FROM teachers WHERE user_id = %s", teacher_tg_id)
        await con.commit()

        if cur.rowcount > 0:
            settings_info = await cur.fetchall()
            return settings_info
        else:
            return False