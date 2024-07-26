import uuid
from django.db import models
from django.conf import settings

from useraccount.models import User

# Create your models here.


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    guests = models.IntegerField()
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    category = models.CharField(max_length=255)

    # image field for favourited properties ...
    image = models.ImageField(upload_to="uploads/properties")
    landlord = models.ForeignKey(
        User, related_name="properties", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        return f"{settings.WEBSITE_URL}{self.image.url}"


# we will need this model to track the reservations ..
class Reservation(models.Model):
    # this will create the reverse relationship called resevations which does 2 things :
    # 1) from properties we can retrieve all reservations on a property
    #
    # 2) from user we can get all reservations made by a user
    #
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # foreign key reference to the property
    property = models.ForeignKey(
        Property, related_name="reservations", on_delete=models.CASCADE
    )
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_nights = models.IntegerField()
    guests = models.IntegerField()
    total_price = models.FloatField()
    # foreign key reference to User model
    created_by = models.ForeignKey(
        User, related_name="reservations", on_delete=models.CASCADE
    )
    # automatically filled out field that tracks when the reservation was created ...
    created_at = models.DateTimeField(auto_now_add=True)
