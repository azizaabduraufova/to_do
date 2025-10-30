from django.contrib import admin

from todo.models import Task, Profile

# Register your models here.

admin.site.register(Task)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'completed')
    readonly_fields = ('created_at',)

admin.site.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio')
    readonly_fields = ('created_at',)