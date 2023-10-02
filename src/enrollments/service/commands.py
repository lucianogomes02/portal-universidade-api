from src.enrollments.service.services import EnrollmentService
from src.libs.command import Command


class EnrollStudentToCourse(Command):
    def add_arguments(self, parser):
        parser.add_argument("student", type=str)
        parser.add_argument("course", type=str)

    def handle(self, *args, **kwargs):
        student_id = args[0].get("student")
        course_id = args[0].get("course")
        return EnrollmentService.enroll_student_to_course(
            course_id=course_id, student_id=student_id
        )
