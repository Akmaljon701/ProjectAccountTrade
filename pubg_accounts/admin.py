from django.contrib import admin

from .models import *


class PubgAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'user_fk']
    list_display_links = ['id', 'type', 'user_fk']
    search_fields = ['type', 'user_fk']
    list_per_page = 20


admin.site.register(PubgAccount, PubgAccountAdmin)


class PubgAccountMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'account_fk', 'file']
    list_display_links = ['id', 'account_fk', 'file']
    search_fields = ['account_fk']
    list_per_page = 20


admin.site.register(PubgAccountMedia, PubgAccountMediaAdmin)
admin.site.register(PubgAccountOrder)
admin.site.register(PubgAccountHistory)
