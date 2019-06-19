from django.contrib import admin
from core.models import Company
# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Company._meta.fields]


