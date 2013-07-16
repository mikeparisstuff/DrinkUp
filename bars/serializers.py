from rest_framework import serializers
from bars.models import Bar, DrinkPrice, Menu
from users.serializers import UserSerializer




class BarSerializer(serializers.ModelSerializer):

    bar_admin = UserSerializer

    class Meta:
        model = Bar


class DrinkPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DrinkPrice

class MenuSerializer(serializers.ModelSerializer):

    drinks = DrinkPriceSerializer(many=True)

    class Meta:
        model = Menu
        fields = (
            'id',
            'name',
            'drinks',
            'created',
            'modified',
        )