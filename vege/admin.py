from django.contrib import admin
from .models import Receipe, ReportCard, StudentID ,Department ,Student, Subject, SubjectMarks
from django.db.models import Sum

# Register your models here.
admin.site.register(Receipe)
admin.site.register(StudentID)
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(ReportCard)

class SubjectMarksDisplay(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks')
    
class ReportCardAdmin(admin.ModelAdmin):
    list_display = ('student', 'student_rank', 'total_marks','date_of_report_card_generation')
    
    def total_marks(self, obj):
        subject_marks = SubjectMarks.objects.filter(student=obj.student)
        marks = subject_marks.aggregate(marks=Sum('marks'))
        return marks['marks']

admin.site.register(SubjectMarks, SubjectMarksDisplay)
