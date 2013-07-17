from rest_framework import serializers
from bars.models import Bar, MenuItem, Menu
from users.serializers import UserSerializer




class BarSerializer(serializers.ModelSerializer):

    bar_admin = UserSerializer

    class Meta:
        model = Bar


class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem

class MenuSerializer(serializers.ModelSerializer):

    menu_items = MenuItemSerializer(many=True)

    class Meta:
        model = Menu
        fields = (
            'id',
            'name',
            'menu_items',
            'created',
            'modified',
        )