from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(Resource),
admin.site.register(Section),
admin.site.register(Session),
admin.site.register(GuideTeacher),
admin.site.register(ClassRegistration),
admin.site.register(ClassInfo),
admin.site.register(PersonalInfo),
admin.site.register(GuardianInfo),
admin.site.register(PreviousAcademicInfo),
admin.site.register(PreviousAcademicCertificate),
admin.site.register(AcademicInfo),
admin.site.register(EnrolledStudent),
admin.site.register(TeacherPersonalInfo),
admin.site.register(Designation),
admin.site.register(ExperienceInfo),
admin.site.register(TrainingInfo),
admin.site.register(EducationInfo),
admin.site.register(Notice),
admin.site.register(TeacherNotice),
admin.site.register(LeaveReportStudent),
admin.site.register(LeaveReportStaff),
admin.site.register(Attendance),
admin.site.register(AttendanceReport),





from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'mobile', 'role' ,'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'mobile', 'photo', 'address', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)

# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)





