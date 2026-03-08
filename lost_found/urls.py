from django.urls import path

from . import views

urlpatterns = [
    path('admin-dashboard-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('reports/', views.reports_overview, name='reports_overview'),
    path('reports/lost/', views.lost_reports_overview, name='lost_reports_overview'),
    path('reports/found/', views.found_reports_overview, name='found_reports_overview'),
    path('claims/', views.claims_overview, name='claims_overview'),
    path('reports/<int:item_id>/approve/', views.approve_report, name='approve_report'),
    path('reports/<int:item_id>/reject/', views.reject_report, name='reject_report'),
    path('claims/submit/', views.claim_item, name='claim_item'),
    path('claims/<int:claim_id>/approve/', views.approve_claim, name='approve_claim'),
    path('claims/<int:claim_id>/reject/', views.reject_claim, name='reject_claim'),
    path('claims/<int:claim_id>/delete/', views.delete_claim, name='delete_claim'),
    path('', views.home, name='home'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('report-lost/', views.report_lost, name='report_lost'),
    path('report-found/', views.report_found, name='report_found'),
    path('search/', views.search_results, name='search_items'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
    path('instructions/', views.instructions, name='instructions'),
]
