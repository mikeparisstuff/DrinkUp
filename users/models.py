import datetime

from django.contrib.auth.models import User

from core.constants import Constants
from django.db import models


class Profile(models.Model):
    '''
    Registered Drinkup User
    '''

    #The Django auth user
    user = models.ForeignKey(
        User
    )

    ROLE_CHOICES=(
        (Constants.USER, "User"),
        (Constants.BAR, "Bar"),
    )

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )

    #: Secret key for profile authentication
    api_secret = models.CharField(
        max_length=255
    )

    #: The user's device token for push notifications
    push_token = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    #: The user's address
    address1 = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    address2 = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    #: The user's city
    city = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    #: The user's state
    state = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    #: The user's zip code
    zip_code = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    #: Last time the user was active on the site
    last_active = models.DateTimeField(
        auto_now_add=False,
        null=True,
        blank=True
    )

    def __unicode__(self):
        return u'Profile {}: {}'.format(self.pk, self.user.email)

    def update_last_active(self):
        self.last_active = datetime.datetime.now()