from faker import Faker
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Group, Teacher, Subject, Mark

fake = Faker()

# Підключення до бази даних
engine = create_engine("postgresql+psycopg2://postgres:secret@localhost:5432/postgres")
Session = sessionmaker(bind=engine)
session = Session()

# Створення таблиць
Base.metadata.create_all(engine)

# Генерація даних
groups = ["Group A", "Group B", "Group C"]
teachers = ["John Doe", "Jane Smith", "Michael Brown"]
subjects = ["Mathematics", "Physics", "Chemistry", "English", "History"]
marks = [2, 3, 4, 5]

# Створення груп
group_objects = []
for group_name in groups:
    group = Group(name=group_name)
    group_objects.append(group)
    session.add(group)
session.commit()

# Створення викладачів
teacher_objects = []
for teacher_name in teachers:
    teacher = Teacher(name=teacher_name)
    teacher_objects.append(teacher)
    session.add(teacher)
session.commit()

# Створення предметів з випадковим призначенням викладачів
subject_objects = []
for subject_name in subjects:
    teacher = random.choice(teacher_objects)
    subject = Subject(name=subject_name, teacher=teacher)
    subject_objects.append(subject)
    session.add(subject)
session.commit()

# Створення студентів з випадковим призначенням груп та оцінок
for _ in range(30, 50):
    student = Student(name=fake.name(), group=random.choice(group_objects))
    session.add(student)
    session.commit()

    for subject in subject_objects:
        for _ in range(random.randint(1, 20)):
            mark_date = fake.date_time_between(start_date="-1y", end_date="now")
            mark = Mark(
                student=student,
                subject=subject,
                date=mark_date,
                mark=random.choice(marks),
            )
            session.add(mark)
    session.commit()
