from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.forms.widgets import SelectMultiple

from core.login import CreateAndReturnNewUser

from users.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''
        Check to see if the Profile object does not have django auth user tied to it.
        This would mean that the profile was created by teh admin panel.
        If this is the case, we want to create and add an auth user.
        '''
        if not obj.user:
            obj.user = CreateAndReturnNewUser()
            obj.save()

        super(ProfileAdmin, self).save_model(request, obj, form, change)

    def first_name(self, the_profile):
        if the_profile.user:
            return '{}'.format(
                the_profile.user.first_name
            )
        else:
            return "none"

    def last_name(self, the_profile):
        if the_profile.user:
            return '{}'.format(the_profile.user.last_name)
        else:
            return 'none'

    list_display = (
        'id',
        'first_name',
        'last_name',
    )

    formfield_overrides = {
        models.ManyToManyField: {'widget': SelectMultiple(attrs={'size':'30'})},
    }

admin.site.register(Profile, ProfileAdmin)