from django.db import models

from core.constants import Constants

class DrinkTransaction(models.Model):
    '''
    Basic drink transaction between a user and bar
    '''

    #: The user making the purchase
    user = models.ForeignKey(
        'users.profile'
    )

    #: The bar selling the merchandise
    bar = models.ForeignKey(
        'bars.Bar'
    )

    is_confirmed = models.BooleanField(
        default=False
    )

    STATUS_CHOICES = (
        (Constants.NEW, "New"),
        (Constants.PENDING, "Pending"),
        (Constants.RECEIVED, "Received"),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=Constants.NEW
    )

    #: The drink item being purchased
    drink = models.ManyToManyField(
        'bars.DrinkPrice'
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    modified = models.DateTimeField(
        auto_now=True
    )