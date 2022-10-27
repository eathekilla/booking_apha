from rest_framework.generics import ListAPIView,CreateAPIView,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderSerializer
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime
from User.models import Users
from .models import Order
import pandas as pd
import requests
import json





def booking_available_list(start_time):
        l = (pd.DataFrame(columns=['NULL'],
                  index=pd.date_range(start_time.replace(hour=7).strftime('%Y-%m-%dT%H:%M:%SZ'), start_time.replace(hour=19).strftime('%Y-%m-%dT%H:%M:%SZ'),
                                      freq='60T'))
       .between_time('07:00','19:00')
       .index.strftime('%Y-%m-%dT%H:%M:%SZ')
       .tolist()
    )
        return l


def bookig_available(start_time,user):
        start = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ').replace(minute=0,second=0,microsecond=0,hour=0)
        end =  start.replace(minute=59,second=0,microsecond=0,hour=23).strftime('%Y-%m-%dT%H:%M:%SZ')
        filters = Q(order_datetime__range=[start.strftime('%Y-%m-%dT%H:%M:%SZ'),end]) & Q(driver__id=user)
        query = Order.objects.filter(filters).values_list('order_datetime', flat=True)
        date_list = list(query)
        date_list = list(map(lambda x: x.strftime('%Y-%m-%dT%H:%M:%SZ').strip(), list(query)))
        lista = booking_available_list(start)
        

        for date in date_list:
            if date in lista:
                lista.remove(date)

        return lista


class OrderList(ListAPIView):
    permission_classes = []
    serializer_class = OrderSerializer
    lookup_field = 'date'
    lookup_url_kwarg = 'date'

    def get_queryset(self):
        date = datetime.strptime(self.kwargs.get('date'), '%Y-%m-%d')
        ordenes = Order.objects.filter(order_datetime__date=date)
            
        return ordenes

    def get(self, request, *args, **kwargs):
        resp = super(OrderList, self).get(request, *args, **kwargs)
        return resp

class OrderListDriver(ListAPIView):
    permission_classes = []
    serializer_class = OrderSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        date = datetime.strptime(self.kwargs.get('date'), '%Y-%m-%d')
        filters = Q(order_datetime__date=date) & Q(driver__id=self.kwargs.get('pk'))
        ordenes = Order.objects.filter(filters)
        return ordenes

    def get(self, request, *args, **kwargs):
        resp = super(OrderListDriver, self).get(request, *args, **kwargs)
        return resp


class CreateOrder(CreateAPIView):
    permission_classes = []
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        disponibilidad = bookig_available(request.data['order_datetime'],request.data['driver'])
        if request.data['order_datetime'].strip() in disponibilidad:
            resp = super(CreateOrder, self).post(request, *args, **kwargs)
            return resp
            
        else:
            return Response({'message': 'No Disponible'}, status=404)
            
            
class SearchDriver(APIView):
    permission_classes = []


    def get(self, request, *args, **kwargs):
        try:
            resp = requests.get('https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json')
            data = resp.json()
            df = pd.DataFrame(data['alfreds'])

            df['distance'] = df.apply(lambda x: ((int(x['lat']) - request.data['lat_pickup'])**2 + (int(x['lng']) - request.data['lng_pickup'])**2)**(1/2), axis=1)
            df = df.sort_values(by='distance')

            for i in range(len(df)):
                driver = df.iloc[i]['id']
                disponibilidad = bookig_available(request.data['order_datetime'],driver)
                if request.data['order_datetime'].strip() in disponibilidad:
                    return Response({'closest_driver': driver}, status=200)

        except Exception as a:
            return Response({'error'}, status=404)

class UpdateDriverUbication(APIView):
    permission_classes = []
    def get(self,request,*args,**kwargs):
        try:
            resp = requests.get('https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json')
            data = resp.json()
            df = pd.DataFrame(data['alfreds'])
            df = df.sort_values(by='id')
            return Response({'drivers': df.to_dict('records')}, status=200)
        except Exception as a:
            return Response({'error'}, status=404)

class ClosestDriver(ListAPIView):
    
    permission_classes = []
    serializer_class = OrderSerializer
    lookup_field = 'datetime'
    lookup_url_kwarg = 'datetime'

    def get_queryset(self):
        date_time = datetime.strptime(self.kwargs.get('datetime'), '%Y-%m-%dT%H:%M:%SZ')
        ordenes = Order.objects.filter(order_datetime=date_time)
        return ordenes

    def get(self, request, *args, **kwargs):
        
        resp = super(ClosestDriver, self).get(request, *args, **kwargs)
        df = pd.DataFrame(resp.data)
        if len(df) > 0:
            df['distance'] = df.apply(lambda x: ((x.lat_pickup - request.data['lat_pickup'])**2 + (x.lng_pickup - request.data['lng_pickup'])**2)**(1/2), axis=1)
            df = df.sort_values(by='distance')

            for i in range(len(df)):
                driver = df.iloc[i]['driver']
                disponibilidad = bookig_available(self.kwargs.get('datetime'),driver)
                if self.kwargs.get('datetime').strip() in disponibilidad:
                    return Response({'closest_driver': driver}, status=200)
        else:
            resp = requests.get('https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json')
            data = resp.json()
            df = pd.DataFrame(data['alfreds'])

            df['distance'] = df.apply(lambda x: ((int(x['lat']) - request.data['lat_pickup'])**2 + (int(x['lng']) - request.data['lng_pickup'])**2)**(1/2), axis=1)
            df = df.sort_values(by='distance')

            for i in range(len(df)):
                driver = df.iloc[i]['id']
                disponibilidad = bookig_available(self.kwargs.get('datetime'),driver)
                if self.kwargs.get('datetime').strip() in disponibilidad:
                    return Response({'closest_driver': driver}, status=200)
        return Response({'No hay conductores disponibles en la fecha indicada'}, status=404)