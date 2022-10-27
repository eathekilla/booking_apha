from django.db import models

class Booking(models.Model):
    order = models.ForeignKey('Order.Order', on_delete=models.CASCADE)
    date_time = models.DateTimeField()

    class Meta:
        verbose_name = ("Booking")
        verbose_name_plural = ("Bookings")

    def __str__(self):
        return self.name
