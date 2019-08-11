from django.contrib import admin

# Register your models here.
from .models import Cmdbs


class CmdbsAdmin(admin.ModelAdmin):
    list_display = ['hostname', 'private_ip', 'vm_status', 'create_time', 'update_time']

    search_fields = ['hostname', 'private_ip']

    list_per_page = 10

    list_filter = ['hostname', 'private_ip']


admin.site.register(Cmdbs, CmdbsAdmin)