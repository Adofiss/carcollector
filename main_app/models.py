from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


# Create your models here.
class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

Types = (
    ('A', 'Level-1'),
    ('B', 'Level-2'),
    ('C', 'Level-3'),
)

class Mod(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()

def __str__(self):
    return self.name

def get_absolute_url(self):
    return reverse('mods_detail', kwargs={'pk': self.id})

class Car(models.Model):
    name = models.CharField(max_length=100)
    hp = models.IntegerField()
    description = models.CharField(max_length=100)
    year = models.IntegerField()
    msrp = models.IntegerField()
    img = models.CharField(max_length=1000)
    mods = models.ManyToManyField(Mod)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

def __str__(self):
    return self.name

# def __str__(self):
#     return f"{self.name} ({self.id})

def get_absolute_url(self):
        return reverse("detail", kwargs={'car_id':self.id})


class Maintenance(models.Model):
    date = models.DateField('maintenance date')
    # mileage = models.CharField(max_length=6)
    type = models.CharField(max_length=1, choices=Types, default=Types[0][0]
                            )

    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_type_display()} on {self.date}"

class Meta:
    ordering = ['-date']


def maintained_for_today(self):
    return self.maintenance_set.filter(date=date.today()).count() >len(Types)