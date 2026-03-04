from django.contrib import admin
from .models import *

class SOAAdmin(admin.ModelAdmin):
    list_display = ('id', 'soa', 'is_effective', 'with_unit', 'reporting', 'is_school', 'is_medical', 'is_outside')
    list_display_links = ('soa',)

# Register your models here.
admin.site.register(SOA, SOAAdmin)
admin.site.register(Position)
admin.site.register(OutsideUnit)
admin.site.register(Report)
admin.site.register(Personnel)
admin.site.register(PersonnelHist)
admin.site.register(Student)
admin.site.register(StudentHist)
admin.site.register(Patient)
admin.site.register(PatientHist)
admin.site.register(ReportComment)
admin.site.register(PersonnelMovement)