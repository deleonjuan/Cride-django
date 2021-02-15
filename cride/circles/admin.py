from django.contrib import admin
from circles.models import Circle
from rides.models import Ride

from django.utils import timezone
import datetime

# Register your models here.
@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    list_display = ('slug_name', 'name', 'is_public', 'is_verified', 'is_limited', 'members_limit')
    search_fields = ('slug_name', 'name')
    list_filter = ('is_public', 'is_verified', 'is_limited')

    actions = ['make_verified', 'make_unverified', 'download_tidays_rides']

    def make_verified(self, ruquest, queryset):
        """ verificar circulos """
        queryset.update(is_verified=True) 
    make_verified.short_description = 'marcar como verificado'

    def make_unverified(self, ruquest, queryset):
        """ quitar el verificado de los circulos """
        queryset.update(is_verified=False) 
    make_unverified.short_description = 'marcar como no verificado'

    def download_tidays_rides(self, request, queryset):
        # now = timezone.now()
        # start = datetime(now.year, now.month, now.day)
        Ride.objects.filter(offered_in__in=queryset.values_list('id'))