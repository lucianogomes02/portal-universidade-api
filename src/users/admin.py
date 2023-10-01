from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Professor, Coordinator

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Coordinator)
