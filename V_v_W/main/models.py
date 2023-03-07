from django.db import models


# Create your models here.

class act_data(models.Model):
    #id = models.IntegerField('id', primary_key=True)
    current_data = models.CharField('current_data', max_length=45)

    class Meta:
        verbose_name = 'Акуальная дата'
        verbose_name_plural = 'Акуальная дата'

    def __str__(self):
        return self.current_data
