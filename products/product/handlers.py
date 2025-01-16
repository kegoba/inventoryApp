
from rest_framework.views import exception_handler
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call the default exception handler to get the standard error response
    response = exception_handler(exc, context)

    # Handle 404 errors specifically
    if response is None:  # If no response from default exception handler
        if isinstance(exc, NotFound):
            return Response(
                {"error": "The resource you are looking for does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

    # If no custom handling, return the default response
    return response
