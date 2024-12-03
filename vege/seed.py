from faker import Faker
import random as r
from .models import Department, Student, StudentID, Subject, SubjectMarks, ReportCard
from django.db.models import Sum
fake = Faker()


def create_subject_mark(n):
    try:
        student_objs = Student.objects.all()
        for student in student_objs:
            subjects = Subject.objects.all()
            for subject in subjects:
                marks = r.randint(0, 100)
                SubjectMarks.objects.create(
                    student=student, subject=subject, marks=marks
                )
    except Exception as e:
        print(e)


def seed_db(n=10) -> None:
    try:
        for i in range(n):
            department_objs = Department.objects.all()
            random_index = r.randint(0, len(department_objs) - 1)
            department = department_objs[random_index]
            student_id = f"STU-00{r.randint(1, 99)}"
            student_name = fake.name()
            student_email = fake.email()
            student_age = r.randint(18, 50)
            student_address = fake.address()

            student_id_obj = StudentID.objects.create(student_id=student_id)

            Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address,
            )
    except Exception as e:
        print(e)


def generate_report_card():
    ranks = Student.objects.annotate(marks=Sum("studentmarks__marks")).order_by(
        "-marks", "-student_age"
    )
    i = 1
    for rank in ranks:
        ReportCard.objects.create(
            student = rank,
            student_rank = i,
        )
        i += 1
