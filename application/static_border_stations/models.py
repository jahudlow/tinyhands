from django.db import models
from dataentry.models import BorderStation


class NullableEmailField(models.EmailField):
    description = "EmailField that stores NULL but returns ''"
    __metaclass__ = models.SubfieldBase
    def to_python(self, value):
        if isinstance(value, models.EmailField):
            return value
        return value or ''
    def get_prep_value(self, value):
        return value or None

class Person(models.Model):
    email = NullableEmailField(blank=True, null=True, default=None, unique=False)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    receives_money_distribution_form = models.BooleanField(default=False)
    border_station = models.ForeignKey(BorderStation, null=True)

    class Meta:
        abstract = True


class Staff(Person):
    class Meta:
        abstract = False



class CommitteeMember(Person):
    class Meta:
        abstract = False


class Location(models.Model):
    name = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    border_station = models.ForeignKey(BorderStation, null=True)