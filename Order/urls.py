from django.urls import path

from Order.views import ClosestDriver, CreateOrder, OrderList,OrderListDriver, SearchDriver

urlpatterns = [
    path('orderlistday/<str:date>/', OrderList.as_view()),
    path('orderdriver/<int:pk>/<str:date>/', OrderListDriver.as_view()),
    path('createorder/', CreateOrder.as_view()),
    path('searchdriver/', SearchDriver.as_view()),
    path('closestdriver/<str:datetime>/', ClosestDriver.as_view()),
]