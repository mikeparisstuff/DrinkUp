from django.contrib import admin

from bars.models import Bar, Drink, MenuItem, Menu

class BarAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'city',
        'state',
        'created',
    )

class DrinkAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'drink_type',
        'created'
    )

class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'drink',
        'price',
        'menu'
    )

class MenuAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created',
        'modified'
    )


admin.site.register(Bar, BarAdmin)
admin.site.register(Drink, DrinkAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Menu, MenuAdmin)