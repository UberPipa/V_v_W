from django.db import models


# Create your models here.

class act_data(models.Model):
    data = models.CharField('current date', max_length=45)

    class Meta:
        verbose_name = 'Акуальная дата'
        verbose_name_plural = 'Акуальная дата'

    def __str__(self):
        return self.data
