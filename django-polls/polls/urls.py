from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<question_hashid>/', views.detail, name='detail'),
    path('<question_hashid>/results/', views.results, name='results'),
    path('<question_hashid>/vote/', views.vote, name='vote'),
]
