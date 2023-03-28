from django.db import models

class Links(models.Model):
    link = models.URLField()

class Dog(models.Model):
    AGE_UNIT = (
        ('m', 'month(s)'),
        ('y', 'year(s)'),
    )
    SEX = (
        ('m', 'male'),
        ('f', 'female'),
    )
    no = models.CharField(max_length=7)
    name = models.CharField(max_length=20)
    breed = models.CharField(max_length=40)
    age = models.IntegerField()
    age_unit = models.CharField(max_length=1, choices=AGE_UNIT)
    gender = models.CharField(max_length=1, choices=SEX)
    weight = models.IntegerField()
    accepted = models.DateField()
    released = models.DateField()
    found_city = models.CharField(max_length=20)
    found_street = models.CharField(max_length=40)
    boxing = models.CharField(max_length=20)
    group_name = models.CharField(max_length=20)
    group_link = models.URLField()
