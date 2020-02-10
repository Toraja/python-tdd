from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^$', views.ListView.as_view(), name='list'),
    url(r'^(\d+)/$', views.ItemView.as_view(), name='list_items'),
]
