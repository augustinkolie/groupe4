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
    path('exports/', views.exports_view, name='exports'),
    path('analyses/', views.analyses_view, name='analyses'),
    
    # Reports & Exports
    path('reports/generate/', views.generate_report, name='generate_report'),
    path('reports/export-excel/', views.export_excel, name='export_excel'),
    path('reports/export-csv/', views.export_csv, name='export_csv'),
    
    # HTMX Partials
    path('partials/stats-overview/', views_htmx.stats_overview, name='stats_overview'),
    path('partials/trigger-api/', views_htmx.trigger_api_fetch, name='trigger_api_fetch'),
    path('partials/map-sync/', views_htmx.map_sync_badge, name='map_sync_badge'),
    path('partials/station-details/<int:station_id>/', views_htmx.station_details_partial, name='station_details_partial'),
    path('partials/station-popup/<int:station_id>/', views_htmx.station_popup_partial, name='station_popup_partial'),
    
    path('accounts/', include('django.contrib.auth.urls')),
]
