from django.contrib import admin
from . models import Student,Teacher,Resource,Class,Section,GuideTeacher,Session,ClassRegistration

# Register your models here.
admin.site.register(Student),
admin.site.register(Teacher),
admin.site.register(Resource),
admin.site.register(Class),
admin.site.register(Section),
admin.site.register(Session),
admin.site.register(GuideTeacher),
admin.site.register(ClassRegistration),