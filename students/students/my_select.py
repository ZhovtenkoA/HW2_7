from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Student, Mark, Subject, Group, Teacher

DB_URI = "postgresql+psycopg2://postgres:secret@localhost:5432/postgres"
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)


def select_1():
    with Session() as session:
        result = (
            session.query(Student)
            .join(Mark)
            .group_by(Student.id)
            .order_by(func.avg(Mark.mark).desc())
            .limit(5)
            .all()
        )
        return result


def select_2(subject):
    with Session() as session:
        result = (
            session.query(Student)
            .join(Mark)
            .join(Subject)
            .filter(Subject.name == subject)
            .group_by(Student.id)
            .order_by(func.avg(Mark.mark).desc())
            .first()
        )
        return result


def select_3(subject):
    with Session() as session:
        query = (
            session.query(Group.name, func.avg(Mark.mark))
            .join(Student, Group.students)
            .join(Mark, Student.marks)
            .join(Subject, Mark.subject)
            .filter(Subject.name == subject)
            .group_by(Group.name)
            .all()
        )
        return query


def select_4():
    with Session() as session:
        result = session.query(func.avg(Mark.mark)).scalar()
        return result


def select_5(teacher_name):
    with Session() as session:
        result = (
            session.query(Subject.name)
            .join(Teacher)
            .filter(Teacher.name == teacher_name)
            .all()
        )
        return result


def select_6(group_name):
    with Session() as session:
        result = (
            session.query(Student).join(Group).filter(Group.name == group_name).all()
        )
        return result


def select_7(group_name, subject_name):
    with Session() as session:
        result = (
            session.query(Student, Mark.mark)
            .join(Group)
            .join(Mark)
            .join(Subject)
            .filter(Group.name == group_name)
            .filter(Subject.name == subject_name)
            .all()
        )
        return result


def select_8(teacher_name):
    with Session() as session:
        average_mark = (
            session.query(func.avg(Mark.mark))
            .join(Subject)
            .join(Teacher)
            .filter(Teacher.name == teacher_name)
            .scalar()
        )

        return average_mark


def select_9(student_id):
    with Session() as session:
        result = (
            session.query(Subject.name)
            .join(Mark)
            .join(Student)
            .filter(Student.id == student_id)
            .all()
        )
        return result


def select_10(student_id, teacher_name):
    with Session() as session:
        result = (
            session.query(Subject.name)
            .join(Mark)
            .join(Student)
            .join(Teacher)
            .filter(Student.id == student_id)
            .filter(Teacher.name == teacher_name)
            .all()
        )
        return result


if __name__ == "__main__":

    # Примеры вызова функций
    print("1")
    result_1 = select_1()
    for student in result_1:
        print(student.name)

    print("2")
    result_2 = select_2(subject="Mathematics")
    if result_2 is not None:
        print(result_2.name)

    print("3")
    result_3 = select_3(subject="Mathematics")
    for group_name, average_mark in result_3:
        print(group_name, average_mark)

    print("4")
    result_4 = select_4()
    print(result_4)

    print("5")
    result_5 = select_5(teacher_name="John Doe")
    unique_courses = set(course.name for course in result_5)
    for subject_name in unique_courses:
        print(subject_name)

    print("6")
    result_6 = select_6(group_name="Group A")
    for student in result_6:
        print(student.name)

    print("7")
    result_7 = select_7(group_name="Group A", subject_name="Mathematics")
    for student, mark in result_7:
        print(student.name, mark)

    print("8")
    average_mark = select_8(teacher_name="Jane Smith")
    print(average_mark)

    print("9")
    result = select_9(student_id=1)
    unique_courses = set(course.name for course in result)
    for course in unique_courses:
        print(course)


    print("10")
    result = select_10(student_id=1, teacher_name="Jane Smith")
    unique_courses = set(course.name for course in result)
    for course in unique_courses:
            print(course)
