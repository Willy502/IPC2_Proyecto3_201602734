from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('loaded', views.load, name="loaded"),
    path('iva_graphics', views.iva_graphic, name="iva_graphics"),
    path('iva_range', views.iva_range, name="iva_range"),
    path('download', views.download, name="download"),
    path('help', views.help, name="help"),
    path('reset', views.reset, name="reset"),
    path('download_doc', views.download_doc, name="download_doc")
]