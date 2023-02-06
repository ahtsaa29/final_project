from django.contrib import admin


# Register your models here.
from userdetails.models import Company, Designation, Payroll, ApplicationType, Application


admin.site.register(Company)
admin.site.register(Designation)
admin.site.register(Payroll)
admin.site.register(ApplicationType)
admin.site.register(Application)