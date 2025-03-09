from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from users.models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'toggle_user_type')
    list_filter = ('user_type',)
    search_fields = ('username', 'email')

    def toggle_user_type(self, obj):
        if obj.user_type == 'professor':
            return format_html('<a class="btn btn-warning" href="{}">Make Student</a>', f'/admin/users/customuser/{obj.id}/make_student/')
        else:
            return format_html('<a class="btn btn-success" href="{}">Make Professor</a>', f'/admin/users/customuser/{obj.id}/make_professor/')

    toggle_user_type.short_description = 'Toggle User Type'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/make_professor/', self.admin_site.admin_view(self.make_professor), name='make_professor'),
            path('<int:user_id>/make_student/', self.admin_site.admin_view(self.make_student), name='make_student'),
        ]
        return custom_urls + urls

    def make_professor(self, request, user_id, *args, **kwargs):
        user = CustomUser.objects.get(pk=user_id)
        user.user_type = 'professor'
        user.save()
        self.message_user(request, f'User {user.username} is now a Professor.')
        return redirect('/admin/users/customuser/')

    def make_student(self, request, user_id, *args, **kwargs):
        user = CustomUser.objects.get(pk=user_id)
        user.user_type = 'student'
        user.save()
        self.message_user(request, f'User {user.username} is now a Student.')
        return redirect('/admin/users/customuser/')

admin.site.register(CustomUser, CustomUserAdmin)
