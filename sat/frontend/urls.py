from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('loaded', views.load, name="loaded"),
    path('iva_graphics', views.iva_graphic, name="iva_graphics")
]