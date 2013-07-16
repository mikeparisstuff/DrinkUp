import hashlib
import uuid
import base64

from django.contrib.auth import logout

from rest_framework.authentication import SessionAuthentication


class APIAuthentication(SessionAuthentication):
    '''
    Provide a custom authentication class that we will specify in our views.

    This will allow us to disable CSRF validation for now.

    TODO: Look into implications of disabling CSRF validation for the API,
    and whethor or not we should re-enable it at a future date.
    '''

    def authenticate(self, request):
        '''
        Returns a User if the request session currently has a logged in user.
        Otherwise returns None.
        '''

        # Get the HttpResponse object
        http_request = request._request
        user = getattr(http_request, 'user', None)

        # Unauthenticated, CSRF validation not required
        if not user or not user.is_active:
            return None

        return(user, None)

