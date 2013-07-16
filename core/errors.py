from rest_framework import status
from rest_framework.response import Response

def New400BadRequest(message):
    return Response(message, status=status.HTTP_400_BAD_REQUEST)
