from django.contrib import admin
from main.models import Server


class ServerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Server, ServerAdmin)
