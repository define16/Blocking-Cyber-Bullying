from django.urls import path, include
from . import views #.은 현재폴더의 디렉토리라는뜻. 즉 현재폴더의 views.py를 import하는것임

urlpatterns = [
    path('', views.index, name='index_user'),
    path('control/', views.control, name='index_control'),
    path('Write', views.Write, name='Write'),
    path('report', views.report, name='report'),
    path('report_o', views.report_o, name='report_o'),
    path('no_bullying', views.no_bullying, name='no_bullying'),
    path('reMakeModul', views.reMakeModul, name='reMakeModul'),
    path('start_learning', views.start_learning, name='start_learning'),
]