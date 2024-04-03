from django.contrib import admin
from .models import Ticket, Department, DepartmentMembership, KnowledgeBase

admin.site.register(Ticket)
admin.site.register(DepartmentMembership)
admin.site.register(KnowledgeBase)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
