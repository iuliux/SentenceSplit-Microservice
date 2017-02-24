from django.conf.urls import url

from .views import sentence_split

urlpatterns = [
    url(r'^$', sentence_split, name='sentence_split'),
]
