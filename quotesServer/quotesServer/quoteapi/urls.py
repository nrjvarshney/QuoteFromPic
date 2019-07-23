from django.conf.urls import url, include
from . import views
urlpatterns = [
                  url('',views.my_view),
               ]