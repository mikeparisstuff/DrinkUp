import json

from django.shortcuts import Http404
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.response import Response

from bars.models import Bar, Drink, MenuItem, Menu
from bars.serializers import BarSerializer, MenuSerializer

from core.constants import Constants
from core.login import HandleFirstTimeLogin
from core.api import AuthenticatedView
from core.api import UnauthenticatedView
from core.validators import validate_bar_unique
from core import errors

from users.models import Profile

class LoginNewBarAdmin(UnauthenticatedView):
    '''
    Create a new bar admin user. Returns the login_token and
    logs the bar admin in.
    '''
    def post(self, request, format=None):
        '''
        email -- Contact email for the bar admin
        password -- Password for the bar admin user
        '''
        bar_admin = HandleFirstTimeLogin(request, Constants.BAR)
        if bar_admin:
            return redirect('/bars/mybar/initiate/')
        return Response(
            '{"detail":"Invalid data to create a new bar admin"}',
            status=status.HTTP_400_BAD_REQUEST
        )

class SetInitialInformation(AuthenticatedView):
    '''
    Set the initial information for the bar after authenticating.
    '''
    serializer_class = BarSerializer

    def post(self, request, format=None):
        '''
        Create and return a new Bar.

        name -- The bar's name
        address1 -- The bar's primary address
        address2 -- (Optional) The bar's secondary address
        city -- The bar's locality
        state -- The bar's state
        zip_code -- The bar's zip_code

        Workflow:
        1. Prompt the bar to create an admin user and log them in.
        2. Prompt the bar for information about their bar and create here.
        '''
        bar_admin = Profile.objects.get(user=request.user)

        try:
            bar = Bar(
                bar_admin = bar_admin,
                name=request.DATA['name'],
                address1=request.DATA['address1'],
                city=request.DATA['city'],
                state=request.DATA['state'],
                zip_code=request.DATA['zip_code']
            )
        except KeyError:
            return Response(
                '{"detail":"A bar must have a name, address1, city, state, and zipcode."}',
                status.HTTP_400_BAD_REQUEST
            )
        try:
            bar.address2 = request.DATA['address2']
        except KeyError:
            pass
        validate_bar_unique(bar)
        menu = Menu.objects.create(
            name="menu_{}".format(bar.name.lower())
        )
        bar.menu = menu
        bar.save()
        serializer = BarSerializer(bar)
        #: After initialization, the bar should be directed to their dashboard. (MyBar)
        # return redirect('/bars/mybar/', status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BarList(UnauthenticatedView):
    '''
    Display a list of all registered Bars.
    '''
    serializer_class = BarSerializer

    def get(self, request, format=None):
        bars = Bar.objects.all()
        serializer = BarSerializer(bars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MyBar(AuthenticatedView):
    '''
    Display information pertaining to the currently logged in bar user's bar.
    '''

    serializer_class = BarSerializer

    def get(self, request, format=None):
        profile = request.user.get_profile()
        bar = Bar.objects.get(bar_admin=profile)
        serializer = BarSerializer(bar)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        '''
        Update the logged in bar's information.

        name -- The bar's name
        address1 -- The bar's primary address
        address2 -- (Optional) The bar's secondary address
        city -- The bar's locality
        state -- The bar's state
        zip_code -- The bar's zip_code
        '''
        profile = request.user.get_profile()
        bar = Bar.objects.get(bar_admin=profile)
        serializer = BarSerializer(bar, data=request.DATA, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class MyMenu(AuthenticatedView):
    """
    Allow the bar to initiate or update their menu offering.
    """
    serializer_class = MenuSerializer
    #: TODO Allow bar to update their menu

    def get(self, request, format=None):
        profile = request.user.get_profile()
        bar = Bar.objects.get(bar_admin=profile)
        serializer = MenuSerializer(bar.menu)
        return Response(serializer.data, status = status.HTTP_200_OK)


    def post(self, request, format=None):
        '''
        On a post, the bar is updating their drink offerings.

        drinks -- (JSON Array) A JSON array holding the drinks to add to the logged in bars menu.
        drink_id --  (int) The Drink object id to be added to the menu via a DrinkPrice object
        drink_price -- (float) The price of the drink offering on the menu.

        The data should come as in the request body in the following format.
        {
            "drinks": [
                {
                    "drink_id":drink_id,
                    "drink_price":price,
                },
                ...
            ]
        }
        '''
        #: TODO: TEST MyMenu
        profile = request.user.get_profile()
        try:
            bar = Bar.objects.get(bar_admin=profile)
            menu = bar.menu
        except Bar.DoesNotExist, Menu.DoesNotExist:
            raise Http404
        data = request.DATA
        try:
            drinks = data['drinks']
            #: For each drink in the post, create a new DrinkPrice and add to menu
            for drink in drinks:
                new_menu_item = MenuItem(
                    drink=Drink.objects.get(pk=drink['drink_id']),
                    price=drink['drink_price'],
                    menu=menu
                )
                new_menu_item.save()
        except KeyError:
            return Response(
                '{"detail":"Post request needs to have a \"drinks\" value."}',
                status = status.HTTP_400_BAD_REQUEST)
        except Drink.DoesNotExist:
            raise Http404
        serializer = MenuSerializer(menu)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



    def put(self, request, format=None):
        '''
        On a put, the bar is updating the prices of already existing drink offerings.
        In the event that the bar is trying to delete items as well, it will take two calls
        to this endpoint ( PUT will update only and DELETE will erase offerings).

        drinks -- JSON array holding the Drink offerings to be updated
        menu_item_id -- The MenuItem object id that needs to be updated
        drink_price -- The new price to update the existing DrinkPrice object.

        Data should come in the following format.
        {
        "drinks": [
           {
              "menu_item_id":drink_id,
              "drink_price":drink_price
           }
           ...
        ]
        }
        Note: These drink_id's must already exist in the DB or else this will 404.
        Also not slight difference between PUT and POST. In PUT, request must supply
        the DrinkPrice object id. In POST, the request gives the Drink object id.
        '''
        #: TODO: On both POST and PUT add a validator to verify that the request is valid.
        profile = request.user.get_profile()
        try:
            menu = Bar.objects.get(bar_admin=profile).menu
        except Bar.DoesNotExist, Menu.DoesNotExist:
            raise Http404
        data = request.DATA
        try:
            drinks = data['drinks']
            #: For each drink in drinks go through and update the entry
            for drink in drinks:
                updated_menu_item = MenuItem.objects.get(pk=drink['menu_item_id'])
                updated_menu_item.price = drink['drink_price']
                updated_menu_item.save()
        except MenuItem.DoesNotExist:
            raise Http404
        except KeyError:
            return Response(
                '{"detail":"Put request requires a \"drinks\" variable in request body"}',
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = MenuSerializer(menu)
        return Response(serializer.data, status=status.HTTP_200_OK)





class BarProfile(UnauthenticatedView):
    '''
    Display information on the bar specified in the url.

    pk -- The corresponding Bar instance id placed in the url.
    '''

    def get(self, request, pk, format=None):
        try:
            bar = Bar.objects.get(pk=pk)
        except Bar.DoesNotExist:
            raise Http404
        serializer = BarSerializer(bar)
        return Response(serializer.data, status=status.HTTP_200_OK)
