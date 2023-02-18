from django.urls import path
from . import views

app_name = "summoner"
urlpatterns = [
    path('<str:region>/<str:s_name>', views.index, name='index'),
]
