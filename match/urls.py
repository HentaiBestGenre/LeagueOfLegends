from django.urls import path
from . import views

app_name = "match"
urlpatterns = [
    path('<str:match_id>', views.index, name='index'),
]
