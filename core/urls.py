from django.conf.urls import url,include
from core.views import (
    dashboard,
company_create,record_list,freelancer_list

)

app_name = 'core'

urlpatterns = [

    url(r'^$', dashboard, name='dashboard'),

    # url(r'^ta', core_ta, name='ta'),

    url(r'^records/', include(([
        url(r'^$', record_list, name='list'),
        url(r'^create$', company_create,name='create'),

        url(r'^(?P<record_pk>\d+)/', include(([
            #url(r'^$', search_summary, name='summary'),

        ],'record'))),
    ],'records'))),

    
    url(r'^freelancers/', include(([
        url(r'^$', freelancer_list, name='list'),
        url(r'^(?P<freelancer_pk>\d+)/', include(([
            #url(r'^$', search_summary, name='summary'),

        ],'freelancer'))),
    ],'freelancers'))),



]
