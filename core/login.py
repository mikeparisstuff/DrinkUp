import uuid
import hashlib

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.http import HttpResponseForbidden

from rest_framework import exceptions
from rest_framework import status
from rest_framework.response import Response

from core.security import create_new_private_key
from core.constants import Constants
from core.base62 import base62_encode
from core.base62 import base62_decode
from core.validators import validate_email_unique
from users.models import Profile
from bars.models import Bar

def AuthUserByToken(request, login_token):
    '''
    Look up user by token and the authenticate via hash routine.
    '''

    try:
        user = User.objects.get(username__exact=login_token)
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed(
            detail="Invalid access_token: {}".format(login_token),
        )

    if user.is_active:
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return
    else:
        raise exceptions.AuthenticationFailed(
            detail='Attempting to login as an inactive user!',
        )

def AuthUserByEmailPassword(request):
    '''
    Look up and authenticate a user by email and password.
    Returns User if successful otherwise None.

    TODO: Make this integrate with the api_secret
    '''
    user = authenticate(
        username=request.DATA['email'],
        password=request.DATA['password']
    )

    if user is not None and user.is_active:
        login(request, user)
        return user
    else:
        return None

def PostLoginHandler(request, created=False):
    '''
    Returns the appropriate response upon login success.
    '''
    login_token = request.user.username
    content = {'login_token': login_token}
    the_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return Response(content, status=the_status)



def CreateAndReturnNewUser(request):
    '''
    Create and return a new user with a random unique identifier as the
    username. To be used for authentication as public access token.
    '''
    access_token = base62_encode(int(uuid.uuid4()))
    try:
        validate_email_unique(request.DATA['email'])
        user = User.objects.create_user(
            access_token,
            request.DATA['email'],
            request.DATA['password'],
        )
    except KeyError:
        raise KeyError('User must have an email, password, and fullname')
    return user


def HandleFirstTimeLogin(request, role):
    '''
    Handles the creation of a new first-time user to the app, returning
    the login token that will be cached on the client side.
    '''
    user = CreateAndReturnNewUser(request)
    if user == None:
        # User already exists with that email
        # TODO: Make this more robust with customized error messages.
        return Response(
            'User already exists at that email or the data was invalid.',
            status = status.HTTP_400_BAD_REQUEST
        )
    else:
        secret_key = create_new_private_key()
        profile = Profile.objects.create(
            user = user,
            role = role,
            api_secret = secret_key
        )
        if profile.role == Constants.USER:
            profile.user.first_name=request.DATA['first_name']
            profile.user.last_name=request.DATA['last_name']
            profile.user.save()
        profile.save()
        AuthUserByToken(request, profile.user.username)

    return PostLoginHandler(
        request,
        created=True
    )
