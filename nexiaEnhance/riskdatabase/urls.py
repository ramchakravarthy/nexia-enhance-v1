from django.urls import path, include

from riskdatabase import views

app_name = 'risk_database'

urlpatterns = [
    # View database
    path('view-risk-database/', views.ViewRiskDatabaseTableView.as_view(), name='view-risk-database'),

    # Import database
    path('import-risk-database/', views.ImportRiskDatabaseView.as_view(), name='import-risk-database'),

    # Update entry
    path('update-category/<pk>', views.RiskDatabaseCatUpdateView.as_view(), name='update-category'),
    path('update-objective/<pk>', views.RiskDatabaseObjectiveUpdateView.as_view(), name='update-objective'),
    path('update-risk/<pk>', views.RiskDatabaseRiskUpdateView.as_view(), name='update-risk'),
    path('update-rr/<pk>', views.RiskDatabaseRiskResponseUpdateView.as_view(), name='update-rr'),

    # Delete entry
    path('delete-category/<pk>', views.RiskDatabaseCatDeleteView.as_view(), name='delete-category'),
    path('delete-objective/<pk>', views.RiskDatabaseObjDeleteView.as_view(), name='delete-objective'),
    path('delete-risk/<pk>', views.RiskDatabaseRiskDeleteView.as_view(), name='delete-risk'),
    path('delete-rr/<pk>', views.RiskDatabaseRRDeleteView.as_view(), name='delete-rr'),

    # Export entry
    path('export_risk_library/', views.RiskDatabaseExportToExcelView, name='export_risk_library'),

]
