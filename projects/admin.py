from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'project_category', 'project_manager', 'start_date', 'estimated_end_date')
    list_display_links = ('project_name', 'project_category', )
    readonly_fields = ('start_date', )


admin.site.register(Project, ProjectAdmin)

