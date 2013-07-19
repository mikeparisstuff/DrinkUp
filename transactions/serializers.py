from payments.models import Charge, Invoice, Customer, ChargeManager

from rest_framework import serializers

class ChargeSerializer(serializers.ModelSerializer):
    '''
    Serializer for a charge
    '''
    # TODO: Depends on Invoice and Customer. May need to include those to be serialized as well.
    # NOTE: Having deep levels of nesting in the serializer can cause latency and speed issues.
    class Meta:
        model = Charge


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice

class CustomerSerializer(serializers.ModelSerializer):
    charges = ChargeSerializer(read_only=True)
    class Meta:
        model = Customer
        fields = (
            'user',
            'card_last_4',
            'card_kind',
            'charges',
        )
        read_only_fields = (
            'user',
            'card_last_4',
            'card_kind',
        )
