from django.db import models

from core.constants import Constants
from users.models import Profile



class Menu(models.Model):
    '''
    A bar's drink menu.
    '''

    #: Name for the menu. By default is menu_{{ bar_name }}
    name = models.CharField(
        max_length=255
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    modified = models.DateTimeField(
        auto_now=True
    )

    def __unicode__(self):
        return u'{}'.format(self.name)


class Bar(models.Model):
    '''
    A registered Bar account
    '''

    #: A bar's admin auth account.
    #: TODO: add CreateAndReturnBarUser to login
    bar_admin = models.ForeignKey(
        Profile
    )

    #: The name of the bar
    name = models.CharField(
        max_length=255
    )

    #: A bar's menu
    menu = models.ForeignKey(
        Menu,
        null=True,
        blank=True
    )

    #: The street address of the bar
    address1 = models.CharField(
        max_length=255,
    )

    #: Secondary street address of the bar
    address2 = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    #: The bar's city:
    city = models.CharField(
        max_length=255
    )

    #: The bar's state:
    state = models.CharField(
        max_length=255
    )

    #: The bar's zipcode
    zip_code = models.CharField(
        max_length=15
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    modified = models.DateTimeField(
        auto_now=True
    )

    def __unicode__(self):
        return u'Bar {}: {}'.format(self.pk, self.name)

class Drink(models.Model):
    '''
    A bar's drink offering.
    '''

    name = models.CharField(
        max_length=255
    )

    DRINK_TYPES = (
        (Constants.BEER, "Beer"),
        (Constants.MIXED_DRINK, "Mixed Drink"),
        (Constants.RAIL, "Rail")
    )

    drink_type = models.CharField(
        max_length=10,
        choices=DRINK_TYPES
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    modified = models.DateTimeField(
        auto_now=True
    )

    def __unicode__(self):
        return u"{}: {}".format(self.name, self.drink_type)


class DrinkPrice(models.Model):
    '''
    Associate a bar's price for an individual drink.
    '''

    drink = models.ForeignKey(Drink)

    price = models.DecimalField(
        decimal_places=2,
        max_digits=7
    )

    menu = models.ForeignKey(
        Menu,
        related_name='drinks'
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    modified = models.DateTimeField(
        auto_now=True
    )

    def __unicode__(self):
        return u'{}: {}'.format(self.price, self.drink)