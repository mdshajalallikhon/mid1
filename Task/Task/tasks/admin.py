from django.contrib import admin
from .models import Employee, Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = ('title', 'due_date', 'status')
    show_change_link = True


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'joining_date', 'pending_tasks')
    search_fields = ('name', 'email')
    list_filter = ('department',)
    inlines = [TaskInline]

    def pending_tasks(self, obj):
        return obj.tasks.filter(status='P').count()
    pending_tasks.short_description = "Pending Tasks"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'days_left', 'due_date')
    search_fields = ('title',)
    list_filter = ('status',)
    raw_id_fields = ('assigned_to',)

    def days_left(self, obj):
        return obj.days_left()
