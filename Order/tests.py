from django.test import TestCase
from .models import Order
from User.models import Users, Driver
import json


class OrderCreate(TestCase):
    @classmethod
    def setUpTestData(cls):
        usuario = Users.objects.create_user(
            email="prueba@a.com",
            first_name="Prueba",
            last_name="Prueba",
        )
        Order.objects.create(
            driver=usuario,
            order_datetime="2022-10-20T08:00:00Z",
            description="Servicio 1",
            lat_pickup=1,
            lng_pickup=-106,
            lat_deliver=251,
            lng_deliver=500

        )
        Order.objects.create(
            driver=usuario,
            order_datetime="2022-10-20T09:00:00Z",
            description="Servicio 1",
            lat_pickup=1,
            lng_pickup=-106,
            lat_deliver=251,
            lng_deliver=500

        )

    def test_crear_orden_con_dispo(self):
        usuario = Users.objects.create_user(
            email="prueba2@a.com",
            first_name="Prueba2",
            last_name="Prueba2",
        )
        body = {
            "driver": 2,
            "order_datetime": "2022-10-20T08:00:00Z",
            "description": "Servicio 2",
            "lat_pickup": 1,
            "lng_pickup": -106,
            "lat_deliver": 251,
            "lng_deliver": 500
        }
        response = self.client.post(
            '/orders/createorder/', data=body, follow=True)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Order.objects.filter(
            description='Servicio 2').count(), 1)

    def test_crear_orden_sin_dispo(self):
        usuario = Users.objects.create_user(
            email="prueba2@a.com",
            first_name="Prueba2",
            last_name="Prueba2",
        )
        body = {
            "driver": 1,
            "order_datetime": "2022-10-20T08:00:00Z",
            "description": "Servicio 3",
            "lat_pickup": 1,
            "lng_pickup": -106,
            "lat_deliver": 251,
            "lng_deliver": 500
        }
        response = self.client.post(
            '/orders/createorder/', data=body, follow=True)
        self.assertEquals(response.status_code, 404)

    def test_get_driver_schedule_day(self):
        date = "2022-10-20"
        id_driver = 1
        resp = self.client.get(
            f'/orders/orderdriver/{id_driver}/{date}/', follow=True)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(Order.objects.filter(
            driver__id=id_driver).count(), len(resp.json()))

    def test_get_closest_driver(self):
        date = "2022-10-23T11:00:00Z"
        body = {
                    "lat_pickup":35,
                    "lng_pickup":0,
                }
        jsons = json.dumps(body,indent = 4)
        resp = self.client.generic(method="GET", path=f'/orders/closestdriver/{date}/', data=json.dumps(body,indent = 4), content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json()['closest_driver'],20)
    
    def test_get_orders_day(self):
        date = "2022-10-20"
        resp = self.client.get(f'/orders/orderlistday/{date}/',follow=True)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(Order.objects.filter(order_datetime__date=date).count(), len(resp.json()))