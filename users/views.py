from django.conf import settings
from django.contrib.auth import logout

from rest_framework import status
from rest_framework.response import Response

from core import errors
from core.api import AuthenticatedView
from core.api import UnauthenticatedView
from core.constants import Constants
from core.login import AuthUserByToken
from core.login import AuthUserByEmailPassword
from core.login import HandleFirstTimeLogin
from core.login import PostLoginHandler
from users.models import Profile
from users.serializers import ProfileSerializer, UserSerializer


class LoginWithToken(UnauthenticatedView):
    '''
    Log in an existing user. Return the login_token and an Http 200 upon success.

    access_token (required) -- Unique public key that identifies a user.
    '''
    def post(self, request, format=None):
        # Try to get a login token from the request
        login_token = request.DATA.get(settings.LOGIN_TOKEN_KEY)

        if login_token:
            # Found token; try to log in user with it
            AuthUserByToken(request, login_token)
            return PostLoginHandler(request)

        if request.user.is_authenticated():
            login_token = request.user.username
            return PostLoginHandler(request)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LoginWithEmail(UnauthenticatedView):
    '''
    Log in an existing user using an email and password.
    Return the login_token and an Http 200 upon success.
    '''
    def post(self, request, format=None):
        if request.user.is_authenticated():
            return PostLoginHandler(request)
        user = AuthUserByEmailPassword(request)
        if user:
            # Found user and logged in.
            return PostLoginHandler(request)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LoginNewUser(UnauthenticatedView):
    '''
    Create and log-in a new user. Returns the login_token and an
    HTTP 201 upon successful user creation.

    Expects a valid email and password
    '''
    def post(self,request, format=None):
        return HandleFirstTimeLogin(request, Constants.USER)

class Logout(AuthenticatedView):
    '''
    Log a user out of the API
    '''
    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        logout(request)
        return Response(status.HTTP_200_OK)

class ProfileList(AuthenticatedView):
    '''
    List all users, or create a new Profile

    TODO: For Debugging purposes, may want to remove
    '''
    serializer_class = ProfileSerializer

    def get(self, request, format=None):
        users = Profile.objects.all()
        serializer = ProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class MyProfile(AuthenticatedView):
    '''
    Retrieve or update the logged-in user's profile.
    '''

    serializer_class = ProfileSerializer

    def get(self, request, format=None):
        my_profile = request.user.get_profile()
        serializer = ProfileSerializer(my_profile)
        return Response(serializer.data)

    def put(self, request, format=None):
        my_profile = request.user.get_profile()

        # User should be able to edit first_name, last_name, email here
        # TODO: Make sure this is safe as we are making two calls to serialize the request
        user_serializer = UserSerializer(
            request.user,
            data=request.DATA,
            partial=True
        )

        if not user_serializer.is_valid():
            return errors.New400BadRequest(user_serializer.errors)
        user_serializer.save()

        serializer = ProfileSerializer(
            my_profile,
            data=request.DATA,
            partial=True
        )
        print serializer.errors
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return errors.New400BadRequest(serializer.errors)