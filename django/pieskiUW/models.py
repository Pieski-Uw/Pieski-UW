from django.db import models


class Pet(models.Model):
    """Model of pet table"""

    SEX = (
        ("m", "male"),
        ("f", "female"),
    )
    no = models.CharField(max_length=7)
    name = models.CharField(max_length=20)
    breed = models.CharField(max_length=40)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=SEX)
    weight = models.IntegerField()
    status = models.CharField(max_length=20)
    date_in = models.DateField()
    date_out = models.DateField()
    address_found = models.CharField(max_length=50)
    box = models.CharField(max_length=20)
    group_name = models.CharField(max_length=20)
    group_link = models.URLField()
    link = models.URLField()
