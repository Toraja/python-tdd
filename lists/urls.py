from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^(\d+)/$', views.ListPageView.as_view(), name='list_items'),
    url(r'^(\d+)/$', views.ItemView.as_view(), name='list_items'),
]
