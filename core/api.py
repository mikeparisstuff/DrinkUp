from rest_framework import permissions
from rest_framework.views import APIView

from authentication import APIAuthentication

class BaseRoundupView(APIView):
    pass
    # def get_serializer_class(self):
    #     '''
    #     Return the serializer class used by the view.
    #
    #     Note: This method is part of GenericAPIView, which is a subclass of the
    #     APIView we are using. It is used by the Django REST Framework Docs app
    #     to determine which field we wish to show in the automatically-generated
    #     API docs.
    #     '''
    #     serializer_class = None
    #     try:
    #         serializer_class = self.serializer_class
    #     except AttributeError:
    #         pass
    #
    #     if serializer_class is None:
    #         class DefaultSerializer(self.model_serializer_class):
    #             class Meta:
    #                 model = self.model
    #         serializer_class = DefaultSerializer
    #
    #     return serializer_class

class UnauthenticatedView(BaseRoundupView):
    '''
    View class for any views which do no require the user to be logged in.
    '''

    # Use our custom authentiation class so that the user doesn't get hit with
    # CSRF errors
    authentication_classes = (APIAuthentication,)

class AuthenticatedView(BaseRoundupView):
    '''
    View class for any views which require the user to be logged in.
    '''

    authentication_classes = (APIAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)