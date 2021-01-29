from django.contrib import admin
from .models import Circle

# Register your models here.
@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    list_display = ('slug_name', 'name', 'is_public', 'is_verified', 'is_limited', 'members_limit')
    search_fields = ('slug_name', 'name')
    list_filter = ('is_public', 'is_verified', 'is_limited')