from django.contrib import admin

from . models import *



admin.site.register(Customer)

@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = (
        'user_type_name',
    )
    
#admin.site.register(Room)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'room_no',
        'name',
        'room_type',
        'availability',
        'display_facility',
        'display_images',
        'staff',
        'adult_count',
        'child_count'
    )
    filter_horizontal = ('conveniences','images',)

admin.site.register(Image)

admin.site.register(Faciliti)

admin.site.register(RoomType)

admin.site.register(Reservation)