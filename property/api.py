from django.http import JsonResponse
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from .models import Property
from .serializers import PropertiesListSerializer


import logging

logger = logging.getLogger("property")


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def property_list(request):
    logger.debug("property_list view called")  # Add log message
    properties = Property.objects.all()
    serializer = PropertiesListSerializer(properties, many=True)

    logger.debug("got the properites count : %s", len(properties))  # Add log message
    logger.debug("*********************************************************")
    logger.debug(f"the property query set returned : {properties}")

    return JsonResponse({"data": serializer.data})
