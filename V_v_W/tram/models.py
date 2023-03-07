from django.db import models

# Create your models here.
class act_data(models.Model):
    data = models.DateField('current date')

    def __str__(self):
        return self.name
