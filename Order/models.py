from turtle import update
from django.db import models
import pandas as pd

class Order(models.Model):
    driver = models.ForeignKey("User.Users", on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    order_datetime = models.DateTimeField(blank=True, null=True)

    lat_pickup = models.IntegerField(blank=True, null=True)
    lng_pickup = models.IntegerField(blank=True, null=True)
    lat_deliver = models.IntegerField(blank=True, null=True)
    lng_deliver = models.IntegerField(blank=True, null=True)

    

    class Meta:
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")

    def __str__(self):
        return f'{self.driver}'


    def booking_available_list(self,start_time):
        l = (pd.DataFrame(columns=['NULL'],
                  index=pd.date_range(start_time.replace(hour=7).strftime('%Y-%m-%dT%H:%M:%SZ'), start_time.replace(hour=19).strftime('%Y-%m-%dT%H:%M:%SZ'),
                                      freq='60T'))
       .between_time('07:00','19:00')
       .index.strftime('%Y-%m-%dT%H:%M:%SZ')
       .tolist()
    )

    def bookig_available(self, start_time):
        date_list = self.objects.all().values_list('order_datetime', flat=True)
        list = self.booking_available_list(start_time)
        lista_eliminada = [e for e in list if e not in date_list]
        print(lista_eliminada)
        return lista_eliminada