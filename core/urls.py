from django.conf.urls import url,include
from core.views import (
    dashboard,
record_create

)

app_name = 'core'

urlpatterns = [

    url(r'^$', dashboard, name='dashboard'),

    # url(r'^ta', core_ta, name='ta'),

    url(r'^records/', include(([
        url(r'^create$', record_create,name='create'),

        url(r'^(?P<record_pk>\d+)/', include(([
            #url(r'^$', search_summary, name='summary'),
            #url(r'^track_node$', search_track_node, name='track_node'),

        ],'record'))),
    ],'records'))),

]
