from django.conf.urls import url
from . import views
from . import consumers


urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    url(r'^$', views.RoomView.as_view()),

]