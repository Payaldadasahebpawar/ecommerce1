from django.contrib import admin
from .models import CustomUser
from django.contrib.admin.models import LogEntry


# Register your models here.


admin.site.register(CustomUser)


class CustomUserAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        # Delete related log entries
        LogEntry.objects.filter(user_id=obj.id).delete()
        # Delete the user
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)

        admin.site.register(CustomUserAdmin)
