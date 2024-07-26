from django.http import JsonResponse
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from .models import Property, Reservation
from .serializers import (
    PropertiesListSerializer,
    PropertiesDetailSerializer,
    ReservationListSerializer,
)
from .forms import PropertyForm

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


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    property = Property.objects.get(pk=pk)

    serialized_data = PropertiesDetailSerializer(property, many=False)

    return JsonResponse(serialized_data.data)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def property_reservations(request, pk):
    # this endpoint will take the property info from the url and will use it to get all reservations existing on it

    property = Property.objects.get(pk=pk)
    reservations = property.reservations.all()

    serialized_data = ReservationListSerializer(reservations, many=True)

    return JsonResponse(serialized_data.data)


@api_view(["POST", "FILES"])
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)

    if form.is_valid():
        property = form.save(commit=False)
        property.landlord = request.user

        property.save()

        return JsonResponse({"success": True})
    else:
        logger.debug("errors %s , %s", form.errors, form.non_field_errors)
        return JsonResponse({"errors": form.errors.as_json()}, status=400)


@api_view(["POST"])
def book_property(request, pk):
    try:
        start_date = request.POST.get("start_date", "")
        end_date = request.POST.get("end_date", "")
        number_of_nights = request.POST.get("number_of_nights", "")
        total_price = request.POST.get("total_price", "")
        guests = request.POST.get("guests", "")

        logger.debug("***************************************************")
        logger.debug("the user object got from url is : %s", request.user)
        logger.debug("***************************************************")

        property = Property.objects.get(pk=pk)
        reservation = Reservation.objects.create(
            property=property,
            start_date=start_date,
            end_date=end_date,
            number_of_nights=number_of_nights,
            total_price=total_price,
            guests=guests,
            created_by=request.user,
        )

        return JsonResponse({"success": True})

    except Exception as e:
        print("Error ", e)
        return JsonResponse({"success": False, "error": str(e)})
