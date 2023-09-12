from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'username', 'first_name', 'phone', 'block', 'role', 'verification_code']
    list_display_links = ('id', 'username', 'first_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('phone', 'block', 'role')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)


class SupportAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_fk', 'get_user_phone', 'text', 'sanded_at_display', 'read']
    list_filter = ['read']
    list_editable = ['read']
    list_display_links = ('id', 'user_fk')
    search_fields = ('id', 'user_fk')
    list_per_page = 20

    def get_user_phone(self, obj):
        return obj.user_fk.phone if obj.user_fk else ''

    get_user_phone.short_description = 'User Phone'

    def sanded_at_display(self, obj):
        return obj.sanded_at.strftime('%Y-%m-%d %H:%M:%S') if obj.sanded_at else ''

    sanded_at_display.short_description = 'Sanded At'


admin.site.register(Support, SupportAdmin)


