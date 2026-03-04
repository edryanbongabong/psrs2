from django.urls import path, re_path
from . import views

urlpatterns = [  
  path('orders/', views.orders_view, name="orders"),
  path('orders/all/', views.OrdersAjaxDatatableView.as_view(), name="view-orders"),
  path('orders/create/', views.OrderCreate.as_view(), name="create-order"),
  path('orders/update/<str:uuid>/', views.OrderUpdate.as_view(), name="update-order"),
  path('orders/delete/<int:pk>/', views.OrderDeleteView.as_view(), name="delete-order"),
]