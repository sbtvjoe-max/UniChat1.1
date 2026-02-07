from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("integrations/", views.integrations, name="integrations"),
    path("security/wipe/", views.wipe_data, name="wipe_data"),
]