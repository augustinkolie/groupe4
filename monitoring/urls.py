from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, views_htmx

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('contact/', views.contact, name='contact'),
    path('features/', views.features, name='features'),
    path('about/', views.about, name='about'),
    path('stations/', views.stations_list, name='stations'),
    path('alerts/', views.alerts_view, name='alerts'),
    path('reports/', views.reports_view, name='reports'),
    
    # HTMX Partials
    path('partials/stats-overview/', views_htmx.stats_overview, name='stats_overview'),
    path('partials/trigger-api/', views_htmx.trigger_api_fetch, name='trigger_api_fetch'),
    
    path('accounts/', include('django.contrib.auth.urls')),
]
