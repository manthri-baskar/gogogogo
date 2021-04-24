from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class past_data(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="past_data")
    good_name   = models.TextField(null=True)
    place       = models.TextField(null=True)
    demand_List = models.TextField(null=True) # JSON-serialized (text) version of your list

    def __str__(self):
        return '{} => {}'.format(self.place, self.good_name) 

class past_csv_data(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="past_csv_data")
    good_name   = models.TextField(null=True)
    place       = models.TextField(null=True)
    demand_List = models.TextField(null=True) # JSON-serialized (text) version of your list

    def __str__(self):
        return '{} => {}'.format(self.place, self.good_name) 

class places(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="places")
    places_List = models.TextField(null=True) 

    def __str__(self):
        return '{}'.format(self.user)