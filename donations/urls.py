from django.urls import path
from . import views

app_name = 'donations' # define el app_name

urlpatterns = [
    path('', views.causa_list, name = 'causa_list'),
    path('causa/<int:causa_id>/', views.causa_detail, name = 'causa_detail'),
    path('causa/nueva/', views.causa_create, name = 'causa_create'),
    path('donar/<int:causa_id>/', views.donar, name = 'donar'),
    path('donacion_exitoso/<int:donacion_id>/', views.donacion_exitoso, name = 'donacion_exitoso'),
    path('causa/eliminar/<int:causa_id>/', views.causa_delete, name = 'causa_delete'),
    path('buscar/', views.buscar_causas, name = 'buscar_causas'),
]
