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
from useraccount.models import User
from rest_framework_simplejwt.tokens import AccessToken

import logging

logger = logging.getLogger("property")


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def property_list(request):
    logger.debug("property_list view called")  # Add log message

    # get the user object based on the token
    try:
        token = request.META["HTTP_AUTHORIZATION"].split("Bearer ")[1]
        token = AccessToken(token)
        user_id = token.payload["user_id"]
        user = User.objects.get(pk=user_id)
    except Exception as e:
        user = None

    # print("checking if user is authed or not ... ", user)

    # if user is not none (ie ; logged in ) then we can get the favourites
    favourites = []
    properties = Property.objects.all()

    if user:
        for property in properties:
            if user in property.favorited.all():
                favourites.append(property.id)
        logger.debug("the favourites for this user is : %s /n/n", favourites)
    else:
        logger.debug("user not logged in ..")

    landlord_id = request.GET.get("landlord_id", "")
    is_favorites = request.GET.get("is_favorites", "")

    if landlord_id:
        logger.debug("property_list for landlord : %s", landlord_id)  # Add log message
        properties = Property.objects.filter(landlord=landlord_id)
    elif is_favorites:
        # this is like a sql query with where in  , here properties , where user in favorited
        properties = Property.objects.filter(favorited__in=[user])
    else:
        # default pick all properties ..
        pass

    serializer = PropertiesListSerializer(properties, many=True)

    logger.debug("got the properites count : %s", len(properties))  # Add log message
    logger.debug("*********************************************************")
    logger.debug(f"the property query set returned : {properties}")

    return JsonResponse({"data": serializer.data, "favourites": favourites})


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

    logger.debug("***************************************************")
    logger.debug("the reservation object is : %s", serialized_data.data)
    logger.debug("***************************************************")

    return JsonResponse(serialized_data.data, safe=False)


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


@api_view(["POST"])
def toggle_favorite(request, pk):
    # endpoint used to set favourite
    property = Property.objects.get(pk=pk)

    if request.user in property.favorited.all():
        # check if the user is one of those who favorited the property
        property.favorited.remove(request.user)
        return JsonResponse({"is_favorite": False})
    else:
        # otherwise add the user to the list of people who favorited the property
        property.favorited.add(request.user)
        return JsonResponse({"is_favorite": True})
