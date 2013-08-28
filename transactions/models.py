import datetime
import stripe

from django.db import models
from django.contrib.auth.models import User

from payments.models import StripeObject

from core.constants import Constants

# class DrinkTransaction(models.Model):
#     '''
#     Basic drink transaction between a user and bar
#     '''
#
#     #: The user making the purchase
#     user = models.ForeignKey(
#         'users.profile'
#     )
#
#     #: The bar selling the merchandise
#     bar = models.ForeignKey(
#         'bars.Bar'
#     )
#
#     is_confirmed = models.BooleanField(
#         default=False
#     )
#
#     STATUS_CHOICES = (
#         (Constants.NEW, "New"),
#         (Constants.PENDING, "Pending"),
#         (Constants.RECEIVED, "Received"),
#     )
#     status = models.CharField(
#         max_length=10,
#         choices=STATUS_CHOICES,
#         default=Constants.NEW
#     )
#
#     # #: The drink item being purchased
#     # drink = models.ManyToManyField(
#     #     'bars.DrinkPrice'
#     # )
#
#     created = models.DateTimeField(
#         auto_now_add=True
#     )
#
#     modified = models.DateTimeField(
#         auto_now=True
#     )

class Recipient(StripeObject):

    #: Django Auth user associated with recipient
    user = models.OneToOneField(User, null=True)

    #: Stripe type token. Either 'individual' or 'corporation'
    recipient_type = models.CharField(
        max_length=50
    )

    #: Optional description for the recipient
    description = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    #: Admin email associated with the recipient
    email = models.EmailField()

    #: The full legal name of the recipient.
    name = models.CharField(
        max_length=255
    )


    #: boolean to verify if the recipient has been verified
    verified = models.BooleanField(
        default=False
    )

    #: The recipient's active account. Either a hash of the account information or null.
    active_account = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    #: Date the stripe recipient was purged
    date_purged = models.DateTimeField(
        null=True,
        blank=True
    )

    #: Date the stripe recipient was created.
    created = models.DateTimeField(
        null=True, editable=False
    )

    def __unicode__(self):
        return unicode("Recipient: {}".format(self.name))

    @property
    def stripe_recipient(self):
        return stripe.Recipient.retrieve(self.stripe_id)

    def purge(self):
        try:
            self.stripe_recipient.delete()
        except stripe.InvalidRequestError as e:
            if e.message.startswith("No such recipient:"):
                pass
            else:
                raise
        self.user = None
        self.active_account = None
        self.date_purged = datetime.now()
        self.name = ""
        self.email = ""
        self.description = ""
        self.save()

    def delete(self, using=None):
        self.purge()

    @classmethod
    def create(cls, user):
        stripe_recipient = stripe.Recipient.create(
            email = user.email,
            type = "corporation"
        )
        recipient = Recipient.objects.create(
            user = user,
            stripe_id = stripe_recipient.id
        )
        return recipient

    def update_bank_account(self):
        recipient = self.stripe_recipient
        