from django.urls import path
from firstapp import views



urlpatterns = [
    path('emps/', views.get_all_charities)
]
